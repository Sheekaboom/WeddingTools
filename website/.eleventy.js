module.exports = function(eleventyConfig) {


    eleventyConfig.addLayoutAlias('default', 'layouts/default.html');

    return {
      templateFormats: ["html","md"],
      dir:{
        input:'site'
      }
    }
  };
