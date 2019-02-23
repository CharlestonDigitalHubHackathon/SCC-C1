function filtertablebyyear(){
    var year = $('#selectedyear').find(":selected").text();

    $.ajax(
            {
                type: "POST",
                data: {
                    btnType: 'filter_by_year',
                    year: year,
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                },
                success: function (data) {
                    // add to table container
                    var tc = $("#tablecontainer");
                    var mylist = data['mylist'];

                    tc.append('<table class="table table-bordered" id="dataTable" width="100%" cellspacing="0">' +
                        '<thead><tr><th style="vertical-align: middle; text-align:center;">Metro Area</th>' +
                        '                                        <th style="text-align:center">Pollutant</th>' +
                        '                                        <th style="vertical-align: middle; text-align:center;">Units of Measurement</th>\n' +
                        '                                        <th style="vertical-align: middle; text-align:center;">\n' +
                        '                                            <a href="https://www.epa.gov/sites/production/files/2014-05/documents/zell-aqi.pdf"\n' +
                        '                                                target="_blank">\n' +
                        '                                                Arithmetic Mean\n' +
                        '                                            </a>\n' +
                        '                                        </th>\n' +
                        '\n' +
                        '                                    </tr>\n' +
                        '                                    </thead>\n' +
                        '\n' +
                        '                                    <tbody>\n');
                    for (var i = 0; i < mylist.length; i++) {
                        mylist[i] = JSON.parse(mylist[i]);
                        tc.append('<tr><td>' + mylist[i].cbsa_name + '</td><td>' + mylist[i].parameter_name + '</td><td>' +
                                    mylist[i].units_of_measure + '</td><td>' + mylist[i].arithmetic_mean + '</td></tr>');
                    }
                    tc.append('</tbody></table>');


                }
            });
}
