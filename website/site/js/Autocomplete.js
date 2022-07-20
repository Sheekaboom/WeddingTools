

export {Autocomplete, load_json_data};

// https://stackoverflow.com/questions/19706046/how-to-read-an-external-local-json-file-in-javascript
function _readTextFile(file, callback) {
    var rawFile = new XMLHttpRequest();
    rawFile.overrideMimeType("application/json");
    rawFile.open("GET", file, true);
    rawFile.onreadystatechange = function() {
        if (rawFile.readyState === 4 && rawFile.status == "200") {
            callback(rawFile.responseText);
        }
    }
    rawFile.send(null);
}

function load_json_data(file_name) {
    var data = "";
    _readTextFile(file_name, function(x) {data = JSON.parse(x)});
    return data;
}

class Autocomplete {

    max_count = 2;
    case_sensitive = false;

    constructor (search_data) {
        this.search_data = search_data;
        this.keys = Object.keys(search_data);
    }

    query (val) {
        var matches = {};
        var count = 0;

        if (val == '') {return matches;}
        if (!this.case_sensitive) {val = val.toLowerCase();}

        for (let i=0; i < this.keys.length; ++i) {

            let cur_key = this.keys[i];   
            let match_val = cur_key;         
            if (!this.case_sensitive) {
                match_val = match_val.toLowerCase();
            } 

            if (match_val.includes(val)) {
                matches[cur_key] = this.search_data[cur_key];
                count = count + 1;
                if (count > this.max_count) {
                    break;
                } 
            }
        }
        return matches;
    }

}