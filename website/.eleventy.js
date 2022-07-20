module.exports = function(eleventyConfig) {


    eleventyConfig.addPassthroughCopy("site/js");
    eleventyConfig.addPassthroughCopy("site/data");

    eleventyConfig.addLayoutAlias('default', 'layouts/default.html');

    return {
      templateFormats: ["html","md"],
      dir:{
        input:'site'
      }
    }
  };
