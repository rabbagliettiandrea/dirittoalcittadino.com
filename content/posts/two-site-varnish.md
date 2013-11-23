date: 2013-10-06
slug: two-site-varnish
title: One machine, two sites. How to handle caching with varnish just for one of them
tags: varnish, nginx

The scenario is the following:
1x EC2 micro-instance that hosts 2 sites, 1 wordpress blog and 1 flask-powered site, say: wpsite.com & flasksite.com.
Both of them are served with nginx that listens on 8080, then varnish listening on 80 that
acts as proxy for nginx.

**What if we have to cache only wpsite.com skipping the cache engine for flasksite.com?**

This an example of a VCL that we could use:

    backend default {
        .host = "127.0.0.1";
        .port = "8080";
    }

    acl purge {
        "127.0.0.1";
    }

    sub vcl_recv {
       if (!req.http.host ~ "^(www\.)?wpsite\.com$") {
    		return(pass);
       }

       remove req.http.X-Forwarded-For;
       set req.http.X-Forwarded-For = client.ip;

       if (req.request == "PURGE") {
         if (!client.ip ~ purge) {
           error 405 "Not allowed.";
         }
         return(lookup);
       }
      if (req.http.Accept-Encoding) {
    	#revisit this list
        if (req.url ~ "\.(gif|jpg|jpeg|swf|flv|mp3|mp4|pdf|ico|png|gz|tgz|bz2)(\?.*|)$") {
          remove req.http.Accept-Encoding;
        } elsif (req.http.Accept-Encoding ~ "gzip") {
          set req.http.Accept-Encoding = "gzip";
        } elsif (req.http.Accept-Encoding ~ "deflate") {
          set req.http.Accept-Encoding = "deflate";
        } else {
          remove req.http.Accept-Encoding;
        }
      }
      if (req.url ~ "\.(gif|jpg|jpeg|swf|css|js|flv|mp3|mp4|pdf|ico|png)(\?.*|)$") {
        unset req.http.cookie;
        set req.url = regsub(req.url, "\?.*$", "");
      }
      if (req.url ~ "\?(utm_(campaign|medium|source|term)|adParams|client|cx|eid|fbid|feed|ref(id|src)?|v(er|iew))=") {
        set req.url = regsub(req.url, "\?.*$", "");
      }
      if (req.http.cookie) {
        if (req.http.cookie ~ "(wordpress_|wp-settings-)") {
          return(pass);
        } else {
          unset req.http.cookie;
        }
      }
    }

    sub vcl_fetch {
      if (req.url ~ "manager" || req.url ~ "wp-(login|admin)" || req.url ~ "preview=true" || req.url ~ "xmlrpc.php") {
        return (hit_for_pass);
      }
      if ( (!(req.url ~ "manager" ||  req.url ~ "(wp-(login|admin)|login)")) || (req.request == "GET") ) {
        unset beresp.http.set-cookie;
       set beresp.ttl = 1h;
      }
      if (req.url ~ "\.(gif|jpg|jpeg|swf|css|js|flv|mp3|mp4|pdf|ico|png)(\?.*|)$") {
        set beresp.ttl = 365d;
      }
    }

    sub vcl_deliver {
       if (obj.hits > 0) {
         set resp.http.X-Cache = "HIT";
       } else {
         set resp.http.X-Cache = "MISS";
       }
    }
    sub vcl_hit {
      if (req.request == "PURGE") {
        set obj.ttl = 0s;
        error 200 "OK";
      }
    }

    sub vcl_miss {
      if (req.request == "PURGE") {
        error 404 "Not cached";
      }
    }

The issue at this point is that all seems to work good but not any sort of
cookie handlers of some sort (like a login-system cookie based).

The key for the resolution of that issue is:

    if (!req.http.host ~ "^(www\.)?wpsite\.com$") {
     return (hit_for_pass);
    }

add the above in vcl_fetch to skip any caching-management for www.wpsite.com.

For better understanding the machinery at the base of that thing follow this [link][1] and
take a look to the chart below, or drop me a line of comment.

[![](/static/images/varnish-flow.png "Varnish flow")][2]

Cheers

[1]: https://www.varnish-cache.org/trac/wiki/VCLExampleDefault
[2]: https://www.varnish-cache.org/trac/attachment/wiki/VCLExampleDefault/varnish-flow.png