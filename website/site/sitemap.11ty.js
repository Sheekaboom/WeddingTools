class Sitemap {

    data(){
        return {
            permalink: "/sitemap.xml",
            eleventyExcludeFromCollections: true  
        }
    }

    render(data){
        return (
//-------------         
`<?xml version="1.0" encoding="utf-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${data.collections.all.map(function(page){
    return(
`    <url>
        <loc>${data.site.url+page.url}</loc>
        <lastmod>${page.date.toISOString()}</lastmod>
        <changefreq>${page.data.changeFreq}</changefreq>
    </url>`)  
}).join('')}
</urlset>
`)
    }
//-------------
}

module.exports = Sitemap;

/*
---
permalink: /sitemap.xml
eleventyExcludeFromCollections: true
---
<?xml version="1.0" encoding="utf-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    {% for page in collections.all %}
        <url>
            <loc>{{ site.url }}{{ page.url | url }}</loc>
            <lastmod>{{ page.date.toISOString() }}</lastmod>
            <changefreq>{{page.data.changeFreq}}</changefreq>
        </url>
    {% endfor %}
</urlset>
*/