function ColorMapService() {
    function mapColor(index, count) {
        var hue = index * 240 / count;
        return 'hsl(' + hue + ',100%,50%)';
    }

    this.generateColorMap = function(societies, query, var_id) {
        var colors = {};
        
        if ('environmental_filters' in query || 'variable_codes' in query) {
            if ('environmental_filters' in query) {
                if (query.environmental_filters[0].id == var_id) {
                    var extractedValues = societies.map(function(society) { return society.environmental_values[0].value; });
                    var min_value = Math.min.apply(null, extractedValues);
                    var max_value = Math.max.apply(null, extractedValues);
                    var range = max_value - min_value;
                    for (var i = 0; i < societies.length; i++) {
                        var society = societies[i];
                        var id = society.society.id;
                        var value = society.environmental_values[0].value;
                        var color = mapColor(value, range);
                        colors[id] = color;
                    }
                }
            } 
            if ('variable_codes' in query) {
                var numCodes = 0;
                var missingData = false;
                for (var i = 0; i < query.variable_codes.length; i++) {
                    if (query.variable_codes[i].variable == var_id) numCodes++;
                }  
                for (var i = 0; i < societies.length; i++) {
                    var society = societies[i];
                    var id = society.society.id;
                    for (var v = 0; v < society.variable_coded_values.length; v++) {
                        if (society.variable_coded_values[v].variable == var_id) {
                            var value = society.variable_coded_values[v].coded_value;
                            if (society.variable_coded_values[v].code_description.description.indexOf("Missing data") != -1) {
                                colors[id] = 'hsl(0, 0%, 100%)';
                                //if (!missingData) numCodes--;
                                missingData = true;
                            } else {
                                var color = mapColor(value, numCodes);
                                colors[id] = color;
                            }
                        } else {
                            continue;
                        }
                    
                    }
                }
            }
        } else if ('language_classifications' in query) {
            var classifications = [];
            for (var i = 0; i < societies.length; i++) {
                //go through societies, add unique classifications to an array
                for (var j = 0; j < societies[i].languages.length; j++) {
                    toAdd = query.language_classifications.filter(function(l) { return l.language.id == societies[i].languages[j].id; });
                    if (toAdd[0] && classifications.indexOf(toAdd[0].class_subfamily) == -1)
                        classifications.push(toAdd[0].class_subfamily);
                }    
            }
            for (var i = 0; i < societies.length; i++) {
                var society = societies[i];
                var id = society.society.id;
                for (var l = 0; l < society.languages.length; l++) {
                    var classification = query.language_classifications.filter(function(m) { return m.language.id == society.languages[l].id; });
                    if (classification[0])
                        var value = classification[0].class_subfamily;
                    var count = classifications.length;
                    var color = mapColor(value, count);
                    colors[id] = color;
                }
            }
        }
        return colors;
    };
}
