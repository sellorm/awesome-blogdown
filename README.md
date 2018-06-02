# Awesome Blogdown
An awesome curated list of blogs built using [blogdown](https://github.com/rstudio/blogdown).

**Update:** Awesome Blogdown has moved to its own site, [awesome-blogdown.com](http://awesome-blogdown.com)!

## About Blogdown

The blogdown package for R lets you create static websites using [RMarkdown](http://rmarkdown.rstudio.com/) and [Hugo](https://gohugo.io/). Sites are rendered to static files which simplifies publishing and hosting, at the same time as allowing you to easily version control your site.

## Contributing to the list

If you want to add a site that uses blogdown to this list, please create a pull request with the necessary change. We'll confirm that it's using blogdown and merge the request. If you're not comfortable doing that, find [me on twitter](https://twitter.com/sellorm) and let me know.

## Adding your site

The Awesome Blogdown website is driven from a single json file that gets deployed to the website. This file is automatically built from the contents of the `json` directory.

To add your site, create a new file in the `json` directory, using the convention '<DOMAIN NAME>.json', for instance, if your site were hosted at 'rstats.example.com' the filename to use would be 'rstats.example.com.json'.

The new file should contain a short json snippet that describes your site. The structure is as follows:

```
{
  "name": "the name of the blog",
  "url": "https://the.url.of.the.blog.com",
  "desc": "A brief description of the blog"
}
```

Have a look at the some of the other files in the `json` directory to get an idea of the structure and what's been added for other sites, and then create a pull request with your changes.

## Using the Awesome Blogdown data

The json file containing all the data is served from [http://awesome-blogdown.com/sites.json](http://awesome-blogdown.com/sites.json).

If you do end up using it for something, let me know, I'd love to hear about it!

## License

MIT  © [Mark Sellors](http://sellorm.com)

