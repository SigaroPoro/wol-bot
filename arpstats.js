"use strict";
$(function() {
    $.ajaxSetup({async: false});
    CheckLoginStatus();
    listArpTables();

    function listArpTables() {
        if ("Expired" != readCookie("SessionStatus")) {
            var goformCbk = "cbGetArpCache";
            $.post("/cgi-bin/" + goformCbk + ".xml",
                    function(rpXML) {
                        listArpTablesCbk(rpXML, goformCbk);
                    },
                    "xml")
                .fail(function(jqXHR, textStatus, errorThrown) {
                    alert(textStatus);
                    alert(errorThrown);
                });
        }
    }

    function listArpTablesCbk(rpXML, goformCbk) {
        $(rpXML).find(goformCbk).each(function() {
            var rt = $(this).find("Result").text();
            if (EXECUTE_OK === rt) {
                $("#ArpTables>table>tbody").empty();
                $(this).find("arp_record").each(function() {
                    var ipaddr = $(this).find("ipaddr").text();
                    var status = $(this).find("status").text();
                    var hwaddr = $(this).find("hwaddr").text();
                    var device = $(this).find("device").text();

                    var tb = $("#ArpTables>table>tbody");
                    var td = '<tr>'
                           + '<td>' + ipaddr + '</td>'
                           + '<td>' + status + '</td>'
                           + '<td>' + hwaddr + '</td>'
                           + '<td>' + device + '</td>'
                           + '</tr>';

                    tb.append(td);

                });
            } else if (EXECUTE_ERROR === rt) {
                //alert(goformCbk + " failed!");
            }
        });
    }

    ////////////////////////////////////////////////////////////////////////

    $("#RefreshTables").click(function() {
        listArpTables();
    });
});
