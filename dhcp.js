"use strict";
$(function() {
    $.ajaxSetup({async: false});
    CheckLoginStatus();
    listDhcpv4ServerPool();

    function listDhcpv4ServerPool() {
        if ("Expired" != readCookie("SessionStatus")) {
            var goformCbk = "cbGetDhcpv4ServerPool";
            $.post("/cgi-bin/" + goformCbk + ".xml",
                    function(rpXML) {
                        listDhcpv4ServerPoolCbk(rpXML, goformCbk);
                    },
                    "xml")
                .fail(function(jqXHR, textStatus, errorThrown) {
                    alert(textStatus);
                    alert(errorThrown);
                });
        }
    }

    function listDhcpv4ServerPoolCbk(rpXML, goformCbk) {
        $(rpXML).find(goformCbk).each(function() {
            var rt = $(this).find("Result").text();
            if (EXECUTE_OK === rt) {
                $(this).find("rtm_cfg_dhcpv4_svr_pool_0i").each(function() {
                    getDhcpv4ServerPool($(this).text(), fillDhcpv4Table);
                });
                $("#DHCPServerList>table>*>tr>*:nth-child(7)").hide();
            } else if (EXECUTE_ERROR === rt) {
                //alert(goformCbk + " failed!");
            }
        });
    }

    ////////////////////////////////////////////////////////////////////////

    function getDhcpv4ServerPool(zi, func) {
        if ("Expired" != readCookie("SessionStatus")) {
            var goformCbk = "cbGetDhcpv4ServerPool";
            $.post("/cgi-bin/" + goformCbk + ".xml", {
                        "rtm_cfg_dhcpv4_svr_pool_0i": zi
                    },
                    function(rpXML) {
                        getDhcpv4ServerPoolCbk(rpXML, goformCbk, zi, func);
                    },
                    "xml")
                .fail(function(jqXHR, textStatus, errorThrown) {
                    alert(textStatus);
                    alert(errorThrown);
                });
        }
    }

    function getDhcpv4ServerPoolCbk(rpXML, goformCbk, zi, func) {
        $(rpXML).find(goformCbk).each(function() {
            var rt = $(this).find("Result").text();
            if (EXECUTE_OK === rt) {
                func(rpXML);
            } else if (EXECUTE_ERROR === rt) {
                //alert(goformCbk + " " + zi + " failed!");
            }
        });
    }

    ////////////////////////////////////////////////////////////////////////

    function fillDhcpv4Table(rpXML) {
        var zi = $(rpXML).find("rtm_cfg_dhcpv4_svr_pool_0i").text();
        var id = $(rpXML).find("rtm_cfg_dhcpv4_svr_pool_id").text();

        var os = $(rpXML).find("opr_status").text();
        var osstr;
        if (os == "0") {
            osstr = "Disabled";
        } else if (os == "1") {
            osstr = "Enabled";
        } else if (os == "2") {
            osstr = "Error";
        } else if (os == "3") {
            osstr = "Misconfigured";
        } else {
            osstr = "UNKNOWN";
        }

        var as = $(rpXML).find("adm_state").text();
        var asstr;
        if (as == "0") {
            asstr = "Disabled";
        } else if (as == "1") {
            asstr = "Enabled";
        } else {
            asstr = "UNKNOWN";
        }

        var ai = $(rpXML).find("ip_intf_id").text();
        var pr = $(rpXML).find("order").text();

        var tb = $("#DHCPServerList>table>tbody");
        var td = '<tr><td><input type="checkbox"></td>' +
            '<td><a href="#">' + zi + '</a></td>' +
            '<td>' + pr + '</td>' +
            '<td>' + osstr + '</td>' +
            '<td>' + asstr + '</td>' +
            '<td>' + ai + '</td>' +
            '<td>' + id + '</td>' +
            '</tr>';
        tb.append(td);

        listIpIntfAll();
    }

    function fillDhcpv4Detail(rpXML) {
        fillFormWithXml("#DHCPServerSettingForm", rpXML);

        $("select[name='order_p']").find("option").removeAttr("selected");
        if ($("input[name='order']").val() == 1) {
            $("select[name='order_p']").find("option").filter("[value=1]").prop("selected", true);
        } else {
            $("select[name='order_p']").find("option").filter("[value=2]").prop("selected", true);
        }

        if ($("input[name='lease_time']").val() == 4294967295) {
            $("input[name='lease_time_u']").prop("checked", true);
        }

        var o = $(rpXML).find("reserved_ipv4").children();
        for (var i = 0, j = 0; i < o.length; i += 2, j++) {
            var ia = o[i + 0].childNodes[0].nodeValue;
            var im = o[i + 1].childNodes[0].nodeValue;
            if (ia != "0.0.0.0") {
                var tb = $("#Tab3_1>table>tbody");
                var td = '<tr><td><input type="checkbox"></td>' +
                    '<td>' + j + '</td>' +
                    '<td>' + ia + '</td>' +
                    '<td>' + im + '</td>' +
                    '</tr>';
                tb.append(td);
            }
        }

        dhcpV4SvrPoolListStatic($(rpXML).find("rtm_cfg_dhcpv4_svr_pool_id").text());
        dhcpV4SvrPoolListOpt($(rpXML).find("rtm_cfg_dhcpv4_svr_pool_id").text());
        dhcpV4SvrPoolListClt($(rpXML).find("rtm_cfg_dhcpv4_svr_pool_id").text());
    }

    ////////////////////////////////////////////////////////////////////////

    $("#DHCPServerSettingForm").submit(function(event) {
        if (check_txtIP() == false) return false;
        if (check_txtMAC() == false) return false;
        if ($("input[name='ipv4_mask-3']").val() != "0") {
            alert("Mask not allowed");
            return false;
        }
        var lease_time = $("input[name='lease_time']").val();
        if (isNaN(lease_time) || (parseInt(lease_time) < 0) || (parseInt(lease_time) > 4294967294)) {
            alert("Lease Time not allowed");
            return false;
        }
        beforeSendForm("#DHCPServerSettingForm");
        var doit = check_txtMASK(0);

        var prp = $("select[name='order_p'] option:selected");
        if (prp.val() == "1") {
            $("input[name='order']").val(1);
        } else if (prp.val() == "3") {
            $("input[name='order']").val(65536);
        }

        if ($("input[name='lease_time_u']").is(":checked")) {
            $("input[name='lease_time']").val(4294967295);
        }

        var ov, ovv;
        ov = $(this).find("[name='dhcpv4_opt61_value']");
        ovv = ov.val();
        if (ovv.length) ov.val(ovv.replace(/\s/g, ""));
        ov = $(this).find("[name='dhcpv4_opt77_value']");
        ovv = ov.val();
        if (ovv.length) ov.val(ovv.replace(/\s/g, ""));

        if (doit) setDhcpv4ServerPool("#DHCPServerSettingForm");

        afterSendForm("#DHCPServerSettingForm");
        event.preventDefault();
    });

    /* reserved ip can only be set in pool. No add/delete support. */
    $("#AddReserveIPForm").submit(function(event) {
        if (check_txtIP() == false) return false;
        beforeSendForm("#AddReserveIPForm");
        var doit = check_txtMASK(2);

        var pool_id = $("#DHCPServerSettingForm").find("[name='rtm_cfg_dhcpv4_svr_pool_id']").val();
        var s = $("#Tab3_1>table>tbody").find("tr:last-child td:nth-child(2)").text();
        $(this).find("[name='rtm_cfg_dhcpv4_svr_pool_id']").val(pool_id);
        var i = (parseInt(s) + 1) || 0;
        var ia = $(this).find("[name='reserved_ipv4_addr']");
        var im = $(this).find("[name='reserved_ipv4_mask']");
        ia.prop("name", "reserved_ipv4_addr" + "_" + i);
        im.prop("name", "reserved_ipv4_mask" + "_" + i);

        if (doit) setDhcpv4ServerPool("#AddReserveIPForm");

        ia.prop("name", "reserved_ipv4_addr");
        im.prop("name", "reserved_ipv4_mask");
        afterSendForm("#AddReserveIPForm");
        event.preventDefault();
    });

    function setDhcpv4ServerPool(selector) {
        if ("Expired" != readCookie("SessionStatus")) {
            $(selector).append('<input type="hidden" name="sessionKey" value="' + sessionKey + '">');
            var goformCbk = "cbSetDhcpv4ServerPool";
            $.post("/cgi-bin/" + goformCbk + ".xml",
                    $(selector).serialize(),
                    function(rpXML) {
                        $(rpXML).find(goformCbk).each(function() {
                            var rt = $(this).find("Result").text();
                            if (EXECUTE_OK !== rt) {
                                //alert($(this).find("ErrorString").text());
                                if ($(this).find("ErrorString").text())
                                    alert($(this).find("ErrorString").text() + ": IP address or subnet mask is not allowed!!");
                            } else {
                                //alert("submitted !!");
                                if ($(this).find("ErrorString").text())
                                    alert($(this).find("ErrorString").text() + ": IP address or subnet mask is not allowed!!");
                            }
                        });
                        window.location.reload();
                    },
                    "xml")
                .fail(function(jqXHR, textStatus, errorThrown) {
                    alert(textStatus);
                    alert(errorThrown);
                });
        }
    }

    $("#AddStaticLeaseForm").submit(function(event) {
        if (check_txtIP() == false) return false;
        if (check_txtMAC() == false) return false;
        beforeSendForm("#AddStaticLeaseForm");

        var pool_id = $("#DHCPServerSettingForm").find("[name='rtm_cfg_dhcpv4_svr_pool_id']").val();
        $(this).find("[name='rtm_cfg_dhcpv4_svr_pool_id']").val(pool_id);

        dhcpV4SvrPoolAddStatic("#AddStaticLeaseForm");
        afterSendForm("#AddStaticLeaseForm");
        event.preventDefault();
    });

    function dhcpV4SvrPoolAddStatic(selector) {
        if ("Expired" != readCookie("SessionStatus")) {
            $(selector).append('<input type="hidden" name="sessionKey" value="' + sessionKey + '">');
            var goformCbk = "cbDhcpV4SvrPoolSetStatic";
            $.post("/cgi-bin/" + goformCbk + ".xml",
                    $(selector).serialize(),
                    function(rpXML) {
                        $(rpXML).find(goformCbk).each(function() {
                            var rt = $(this).find("Result").text();
                            if (EXECUTE_OK !== rt) {
                                alert($(this).find("ErrorString").text());
                            } else {
                                //alert("submitted !!");
                            }
                        });
                        window.location.reload();
                    },
                    "xml")
                .fail(function(jqXHR, textStatus, errorThrown) {
                    alert(textStatus);
                    alert(errorThrown);
                });
        }
    }

    $("#AddOptionForm").submit(function(event) {
        var oc = $(this).find("[name='opt_code']");
        var ol = $(this).find("[name='opt_len']");
        var ov = $(this).find("[name='opt_value']");
        var ocv = oc.val();
        var olv = ol.val();
        var ovv = ov.val();
        if (parseInt(ocv) < 255) {
            var pool_id = $("#DHCPServerSettingForm").find("[name='rtm_cfg_dhcpv4_svr_pool_id']").val();
            $(this).find("[name='rtm_cfg_dhcpv4_svr_pool_id']").val(pool_id);
            if (parseInt(ocv) < 224) {
                if (ovv.length) ov.val(ovv.replace(/\s/g, ""));
            } else {
                if (ovv.length) ov.val(str2hex(ovv));
            }
            if (!olv.length) ol.val(Math.floor(ov.val().length/2));
            dhcpV4SvrPoolAddOption("#AddOptionForm");
        }
        event.preventDefault();
    });

    function dhcpV4SvrPoolAddOption(selector) {
        if ("Expired" != readCookie("SessionStatus")) {
            $(selector).append('<input type="hidden" name="sessionKey" value="' + sessionKey + '">');
            var goformCbk = "cbDhcpV4SvrPoolSetOpt";
            $.post("/cgi-bin/" + goformCbk + ".xml",
                    $(selector).serialize(),
                    function(rpXML) {
                        $(rpXML).find(goformCbk).each(function() {
                            var rt = $(this).find("Result").text();
                            if (EXECUTE_OK !== rt) {
                                alert($(this).find("ErrorString").text());
                            } else {
                                //alert("submitted !!");
                            }
                        });
                        window.location.reload();
                    },
                    "xml")
                .fail(function(jqXHR, textStatus, errorThrown) {
                    alert(textStatus);
                    alert(errorThrown);
                });
        }
    }

    ////////////////////////////////////////////////////////////////////////

    function getDhcpV4SvrPoolStatic(pool_id, static_id) {
        if ("Expired" != readCookie("SessionStatus")) {
            var goformCbk = "cbDhcpV4SvrPoolGetStatic";
            $.post("/cgi-bin/" + goformCbk + ".xml", {
                        "rtm_cfg_dhcpv4_svr_pool_id": pool_id,
                        "rtm_dhcpv4_svr_pool_static_id": static_id
                    },
                    function(rpXML) {
                        $(rpXML).find(goformCbk).each(function() {
                            var rt = $(this).find("Result").text();
                            if (EXECUTE_OK === rt) {
                                fillFormWithXml("#AddStaticLeaseForm", rpXML);
                            } else if (EXECUTE_ERROR === rt) {
                            }
                        });
                    },
                    "xml")
                .fail(function(jqXHR, textStatus, errorThrown) {
                    alert(textStatus);
                    alert(errorThrown);
                });
        }
    }

    function dhcpV4SvrPoolListStatic(id) {
        if ("Expired" != readCookie("SessionStatus")) {
            var goformCbk = "cbDhcpV4SvrPoolGetStatic";
            $.post("/cgi-bin/" + goformCbk + ".xml", {
                        "rtm_cfg_dhcpv4_svr_pool_id": id,
                        "all": "ALL"
                    },
                    function(rpXML) {
                        dhcpV4SvrPoolListStaticCbk(rpXML, goformCbk);
                    },
                    "xml")
                .fail(function(jqXHR, textStatus, errorThrown) {
                    alert(textStatus);
                    alert(errorThrown);
                });
        }
    }

    function dhcpV4SvrPoolListStaticCbk(rpXML, goformCbk) {
        $(rpXML).find(goformCbk).each(function() {
            var rt = $(this).find("Result").text();
            if (EXECUTE_OK === rt) {
                $(rpXML).find("rtm_dhcpv4_svr_pool_static").each(function() {
                    var id = $(this).find("rtm_dhcpv4_svr_pool_static_id").text();
                    var as = $(this).find("adm_state").text();
                    var asstr;
                    if (as == "0") asstr = "Disabled";
                    else asstr = "Enabled";
                    var ma = $(this).find("mac_addr").text();
                    var ia = $(this).find("ipv4_addr").text();

                    var tb = $("#Tab2_1>table>tbody");
                    var td = '<tr><td><input type="checkbox"></td>' +
                        '<td><a href="#">' + id + '</a></td>' +
                        '<td>' + ma + '</td>' +
                        '<td>' + ia + '</td>' +
                        '<td>' + asstr + '</td>' +
                        '</tr>';
                    tb.append(td);
                });
                $(document).on('click','#Tab2_1 a',function() {
                    var pool_id = $("#DHCPServerSettingForm").find("[name='rtm_cfg_dhcpv4_svr_pool_id']").val();
                    var static_id = $(this).text();
                    $("#AddStatic").click();
                    getDhcpV4SvrPoolStatic(pool_id, static_id);
                });
            } else if (EXECUTE_ERROR === rt) {
                //alert(goformCbk + " failed!");
            }
        });
    }

    ////////////////////////////////////////////////////////////////////////

    function getDhcpV4SvrPoolOpt(pool_id, option_id) {
        if ("Expired" != readCookie("SessionStatus")) {
            var goformCbk = "cbDhcpV4SvrPoolGetOpt";
            $.post("/cgi-bin/" + goformCbk + ".xml", {
                        "rtm_cfg_dhcpv4_svr_pool_id": pool_id,
                        "rtm_dhcpv4_svr_pool_opt_id": option_id
                    },
                    function(rpXML) {
                        $(rpXML).find(goformCbk).each(function() {
                            var rt = $(this).find("Result").text();
                            if (EXECUTE_OK === rt) {
                                fillFormWithXml("#AddOptionForm", rpXML);
                            } else if (EXECUTE_ERROR === rt) {
                            }
                        });
                    },
                    "xml")
                .fail(function(jqXHR, textStatus, errorThrown) {
                    alert(textStatus);
                    alert(errorThrown);
                });
        }
    }

    function dhcpV4SvrPoolListOpt(id) {
        if ("Expired" != readCookie("SessionStatus")) {
            var goformCbk = "cbDhcpV4SvrPoolGetOpt";
            $.post("/cgi-bin/" + goformCbk + ".xml", {
                        "rtm_cfg_dhcpv4_svr_pool_id": id,
                        "all": "ALL"
                    },
                    function(rpXML) {
                        dhcpV4SvrPoolListOptCbk(rpXML, goformCbk);
                    },
                    "xml")
                .fail(function(jqXHR, textStatus, errorThrown) {
                    alert(textStatus);
                    alert(errorThrown);
                });
        }
    }

    function dhcpV4SvrPoolListOptCbk(rpXML, goformCbk) {
        $(rpXML).find(goformCbk).each(function() {
            var rt = $(this).find("Result").text();
            if (EXECUTE_OK === rt) {
                $(rpXML).find("rtm_dhcpv4_svr_pool_opt").each(function() {
                    var id = $(this).find("rtm_dhcpv4_svr_pool_opt_id").text();
                    var as = $(this).find("adm_state").text();
                    var asstr;
                    if (as == "0") asstr = "Disabled";
                    else asstr = "Enabled";
                    var oc = $(this).find("opt_code").text();
                    var ol = $(this).find("opt_len").text();
                    var od = $(this).find("opt_value").text();
                    if (parseInt(oc) >= 224)
                        if (od.length)
                            od = hex2str(od.replace(/\s/g, ""));

                    var tb = $("#Tab4_1>table>tbody");
                    var td = '<tr><td><input type="checkbox"></td>' +
                        '<td><a href="#">' + id + '</a></td>' +
                        '<td>' + oc + '</td>' +
                        '<td>' + ol + '</td>' +
                        '<td>' + od + '</td>' +
                        '<td>' + asstr + '</td>' +
                        '</tr>';
                    tb.append(td);
                });
                $(document).on('click','#Tab4_1 a',function() {
                    var pool_id = $("#DHCPServerSettingForm").find("[name='rtm_cfg_dhcpv4_svr_pool_id']").val();
                    var option_id = $(this).text();
                    $("#AddOption").click();
                    getDhcpV4SvrPoolOpt(pool_id, option_id);
                });
            } else if (EXECUTE_ERROR === rt) {
                //alert(goformCbk + " failed!");
            }
        });
    }

    ////////////////////////////////////////////////////////////////////////

    function dhcpV4SvrPoolListClt(id) {
        if ("Expired" != readCookie("SessionStatus")) {
            var goformCbk = "cbDhcpV4SvrPoolGetClt";
            $.post("/cgi-bin/" + goformCbk + ".xml", {
                        "rtm_cfg_dhcpv4_svr_pool_id": id,
                        "all": "ALL"
                    },
                    function(rpXML) {
                        dhcpV4SvrPoolListCltCbk(rpXML, goformCbk);
                    },
                    "xml")
                .fail(function(jqXHR, textStatus, errorThrown) {
                    alert(textStatus);
                    alert(errorThrown);
                });
        }
    }

    function dhcpV4SvrPoolListCltCbk(rpXML, goformCbk) {
        $(rpXML).find(goformCbk).each(function() {
            var rt = $(this).find("Result").text();
            if (EXECUTE_OK === rt) {
                $(rpXML).find("rtm_dhcpv4_svr_pool_clt").each(function() {
                    var id = $(this).find("rtm_dhcpv4_svr_pool_clt_id").text();
                    var ma = $(this).find("mac_addr").text();
                    var act = $(this).find("is_active").text();
                    var actstr;
                    if (act == "0") actstr = "Deactive";
                    else actstr = "Active";

                    var opt = "";
                    $(this).find("rtm_dhcpv4_svr_pool_clt_opt").each(function() {
                        var val = $(this).find("dhcpv4_opt").text();
                        opt += $(this).find("dhcpv4_opt").text() + "&#13;&#10;";
                    });

                    var tb = $("#Tab5>table>tbody");
                    $(this).find("rtm_dhcpv4_svr_pool_clt_addr").each(function() {
                        var ia = $(this).find("ipv4_addr").text();
                        var lrt = $(this).find("lease_remaining").text();
                        var td = '<tr>' +
                            '<td>' + ma + '</td>' +
                            '<td>' + ia + '</td>' +
                            '<td>' + actstr + '</td>' +
                            '<td>' + lrt + '</td>' +
                            '<td><abbr title="' + opt + '">More</abbr></td>' +
                            '</tr>';
                        tb.append(td);
                    });
                });
            } else if (EXECUTE_ERROR === rt) {
                //alert(goformCbk + " failed!");
            }
        });
    }

    ////////////////////////////////////////////////////////////////////////

    function listIpIntfAll() {
        if ("Expired" != readCookie("SessionStatus")) {
            var goformCbk = "cbGetIpIntf";
            $.post("/cgi-bin/" + goformCbk + ".xml", {
                        "all": "ALL"
                    },
                    function(rpXML) {
                        listIpIntfCbk(rpXML, goformCbk);
                    },
                    "xml")
                .fail(function(jqXHR, textStatus, errorThrown) {
                    alert(textStatus);
                    alert(errorThrown);
                });
        }
    }

    function listIpIntfCbk(rpXML, goformCbk) {
        $(rpXML).find(goformCbk).each(function() {
            var rt = $(this).find("Result").text();
            if (EXECUTE_OK === rt) {
                $("#IPIntfId").empty();
                $(rpXML).find("rtm_cfg_ip_intf").each(function() {
                    if ($(this).find("type").text() != 2) {
                        return true;
                    }
                    var id = $(this).find("rtm_cfg_ip_intf_id").text();
                    var nm = $(this).find("name").text().escape();
                    // prepare pull down list for associated Interface in DHCPServerShow
                    var opt = '<option value="' + id + '">' + nm + '</option>';
                    $("#IPIntfId").append(opt);
                    // replace associated Interface in DHCPServerList
                    $("#DHCPServerList>table>tbody>tr").each(function() {
                        var o = $(this).find("td:eq(5)");
                        if (o.text() == id) {
                            o.text(nm);
                        }
                    });
                });
            } else if (EXECUTE_ERROR === rt) {
                //alert(goformCbk + " failed!");
            }
        });
    }

    ////////////////////////////////////////////////////////////////////////

    $("#DelPool").click(function() {
        $("#DHCPServerList>table>tbody").find("tr").each(function(rowIndex, r) {
            if ($(r).find("td:first-child>input").is(":checked")) {
                var pool_id = $(r).find("td:nth-child(7)").text();
                if ("Expired" != readCookie("SessionStatus")) {
                    var goformCbk = "cbSetDhcpv4ServerPool";
                    $.post("/cgi-bin/" + goformCbk + ".xml", {
                                "del": "DEL",
                                "rtm_cfg_dhcpv4_svr_pool_id": pool_id,
                                "sessionKey": sessionKey
                            },
                            function(rpXML) {
                                $(rpXML).find(goformCbk).each(function() {
                                    var rt = $(this).find("Result").text();
                                    if (EXECUTE_OK !== rt) {
                                        alert($(this).find("ErrorString").text());
                                    } else {
                                        //alert("submitted !!");
                                    }
                                });
                            },
                            "xml")
                        .fail(function(jqXHR, textStatus, errorThrown) {
                            alert(textStatus);
                            alert(errorThrown);
                        });
                }
            }
        });
        window.location.reload();
    });

    $("#AddPool").click(function() {
        if ("Expired" != readCookie("SessionStatus")) {
            var goformCbk = "cbSetDhcpv4ServerPool";
            $.post("/cgi-bin/" + goformCbk + ".xml", {
                        "sessionKey": sessionKey
                    },
                    function(rpXML) {
                        $(rpXML).find(goformCbk).each(function() {
                            var rt = $(this).find("Result").text();
                            if (EXECUTE_OK !== rt) {
                                alert($(this).find("ErrorString").text());
                            } else {
                                //alert("submitted !!");
                            }
                        });
                        window.location.reload();
                    },
                    "xml")
                .fail(function(jqXHR, textStatus, errorThrown) {
                    alert(textStatus);
                    alert(errorThrown);
                });
        }
    });

    $("#DelStatic").click(function() {
        var pool_id = $("#DHCPServerSettingForm").find("[name='rtm_cfg_dhcpv4_svr_pool_id']").val();
        $("#Tab2_1>table>tbody").find("tr").each(function(rowIndex, r) {
            if ($(r).find("td:first-child>input").is(":checked")) {
                var static_id = $(r).find("td:nth-child(2)").text();
                if ("Expired" != readCookie("SessionStatus")) {
                    var goformCbk = "cbDhcpV4SvrPoolSetStatic";
                    $.post("/cgi-bin/" + goformCbk + ".xml", {
                                "del": "DEL",
                                "rtm_cfg_dhcpv4_svr_pool_id": pool_id,
                                "rtm_dhcpv4_svr_pool_static_id": static_id,
                                "sessionKey": sessionKey
                            },
                            function(rpXML) {
                                $(rpXML).find(goformCbk).each(function() {
                                    var rt = $(this).find("Result").text();
                                    if (EXECUTE_OK !== rt) {
                                        alert($(this).find("ErrorString").text());
                                    } else {
                                        //alert("submitted !!");
                                    }
                                });
                            },
                            "xml")
                        .fail(function(jqXHR, textStatus, errorThrown) {
                            alert(textStatus);
                            alert(errorThrown);
                        });
                }
            }
        });
        window.location.reload();
    });

    $("#AddStatic").click(function() {
        $("#Tab2_1").css("display", "none");
        $("#Tab2_2").css("display", "block");
    });

    /* reserved ip can only be set in pool. No add/delete support. */
    $("#DelReserve").click(function() {
        var pool_id = $("#DHCPServerSettingForm").find("[name='rtm_cfg_dhcpv4_svr_pool_id']").val();
        $("#Tab3_1>table>tbody").find("tr").each(function(rowIndex, r) {
            if ($(r).find("td:first-child>input").is(":checked")) {
                var obj_list = {
                    "sessionKey": sessionKey,
                    "rtm_cfg_dhcpv4_svr_pool_id": pool_id
                };
                var reserved_zi = $(r).find("td:nth-child(2)").text();
                var ia = "reserved_ipv4_addr_" + reserved_zi;
                var im = "reserved_ipv4_mask_" + reserved_zi;
                obj_list[ia] = "0.0.0.0";
                obj_list[im] = "0.0.0.0";
                if ("Expired" != readCookie("SessionStatus")) {
                    var goformCbk = "cbSetDhcpv4ServerPool";
                    $.post("/cgi-bin/" + goformCbk + ".xml",
                            obj_list,
                            function(rpXML) {
                                $(rpXML).find(goformCbk).each(function() {
                                    var rt = $(this).find("Result").text();
                                    if (EXECUTE_OK !== rt) {
                                        alert($(this).find("ErrorString").text());
                                    } else {
                                        //alert("submitted !!");
                                    }
                                });
                            },
                            "xml")
                        .fail(function(jqXHR, textStatus, errorThrown) {
                            alert(textStatus);
                            alert(errorThrown);
                        });
                }
            }
        });
        window.location.reload();
    });

    $("#AddReserve").click(function() {
        $("#Tab3_1").css("display", "none");
        $("#Tab3_2").css("display", "block");
    });

    $("#DelOption").click(function() {
        var pool_id = $("#DHCPServerSettingForm").find("[name='rtm_cfg_dhcpv4_svr_pool_id']").val();
        $("#Tab4_1>table>tbody").find("tr").each(function(rowIndex, r) {
            if ($(r).find("td:first-child>input").is(":checked")) {
                var obj_list = {
                    "sessionKey": sessionKey,
                    "rtm_cfg_dhcpv4_svr_pool_id": pool_id
                };
                var option_id = $(r).find("td:nth-child(2)").text();
                obj_list["rtm_dhcpv4_svr_pool_opt_id"] = option_id;
                obj_list["del"] = "DEL";
                if ("Expired" != readCookie("SessionStatus")) {
                    var goformCbk = "cbDhcpV4SvrPoolSetOpt";
                    $.post("/cgi-bin/" + goformCbk + ".xml",
                            obj_list,
                            function(rpXML) {
                                $(rpXML).find(goformCbk).each(function() {
                                    var rt = $(this).find("Result").text();
                                    if (EXECUTE_OK !== rt) {
                                        alert($(this).find("ErrorString").text());
                                    } else {
                                        //alert("submitted !!");
                                    }
                                });
                            },
                            "xml")
                        .fail(function(jqXHR, textStatus, errorThrown) {
                            alert(textStatus);
                            alert(errorThrown);
                        });
                }
            }
        });
        window.location.reload();
    });

    $("#AddOption").click(function() {
        $("#Tab4_1").css("display", "none");
        $("#Tab4_2").css("display", "block");
        if (tef)
            $("#tef").css("display", "block");
        else
            $("#std").css("display", "block");
    });

    // auto hook event to dynamic created element
    $("#DHCPServerList a").click(function() {
        $("#DHCPServerShow>legend").text($(this).text());
        InitDisplay();
        listIpIntfAll();
        getDhcpv4ServerPool($(this).text(), fillDhcpv4Detail);
    });

    ////////////////////////////////////////////////////////////////////////

    function InitDisplay() {
        $("#DHCPServerList").css("display", "none");
        $("#DHCPServerShow").css("display", "block");
    }

    function hex2str(hexx) {
        var hex = hexx.toString(); //force conversion
        var str = '';
        for (var i = 0; i < hex.length; i += 2)
            str += String.fromCharCode(parseInt(hex.substr(i, 2), 16));
        return str;
    }

    function str2hex(str) {
        var arr = [];
        for (var i = 0, l = str.length; i < l; i ++) {
            var hex = Number(str.charCodeAt(i)).toString(16);
            arr.push(hex);
        }
        return arr.join('');
    }
});
