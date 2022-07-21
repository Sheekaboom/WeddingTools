module.exports = function(eleventyConfig) {


    eleventyConfig.addPassthroughCopy("site/js");
    eleventyConfig.addPassthroughCopy("site/data");
    eleventyConfig.addPassthroughCopy("site/css");
    eleventyConfig.addPassthroughCopy("site/img");

    eleventyConfig.addLayoutAlias('default', 'layouts/default.html');

    return {
      templateFormats: ["html","md"],
      dir:{
        input:'site'
      }
    }
  };
