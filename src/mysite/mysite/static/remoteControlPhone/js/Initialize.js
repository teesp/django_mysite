(function() {
    $(document).ready(function() {
        // var deviceList = $('.deviceItem')
        // for (var i = 0; i < deviceList.length; i++) {
        // var button_send = deviceList.eq(i).find('button.send')
        // button_send.click(function() {
        // var regId = $(this).attr('regId')
        // var getObj = {
        // "regId" : regId,
        // "data" : {
        // "showText" : "this is a text message hoping sent to phone"
        // }
        // }
        // var getStr = JSON.stringify(getObj);
        //
        // $.ajax({
        // type : "POST",
        // url : '/remoteControlPhone/pushToPhone/',
        // data : getStr,
        // success : function() {
        // alert("send success")
        // },
        // dataType : "html"
        // });
        // })
        // };
        Initialize()        InitializeGlobalVariable()
        InitializeEvent()
    })
    function InitializeGlobalVariable() {
        GetCallLogs(function(data) {
            callLogsGlobal = $.parseJSON(data);
        })
    }

    function InitializeEvent() {
        // $('.ICON_sendSMS').click(function() {
            // $(this).tooltip('show')
        // })
    }


    window.callLogsGlobal = null;
    window.checkTimeInterval = 4000;
    window.checkMaxTimes = 10;

    function Initialize() {
        var updateStatusButton = $('#tab1 .updateStatusButton');
        var updateStatusWording = $('#tab1 .updateStatusWording');
        var updateStatusloadingAnimation = $('#tab1 .loadingAnimation');

        updateStatusButton.click(function() {
            updateStatusWording.text("Send Request to Google Cloud");
            updateStatusButton.attr("disabled", true);
            updateStatusloadingAnimation.show();

            SendMessageToGCM(function() {
                updateStatusWording.text("Message has been sent to GCM successfully, now wait for device's response");

                // check whether the data has updated every 5 seconds.
                CheckDataUpdated(0);
            }, function() {
                console.error("Send message to GCM encounter error");
            })
        })
        function CheckDataUpdated(currentTry) {
            currentTry++;
            if (currentTry > checkMaxTimes) {
                updateStatusWording.text("Timeout. Please try again later");
                updateStatusButton.attr("disabled", false);
                updateStatusloadingAnimation.hide();
                return;
            }

            setTimeout(function() {
                GetCallLogs(function(data) {
                    // check if the data has updated by comparing the timestamp.
                    var jsonData = $.parseJSON(data)
                    if (jsonData.length > 0 && parseFloat(jsonData[0].date_created) > parseFloat(callLogsGlobal[0].date_created)) {
                        callLogsGlobal = jsonData;
                        updateStatusWording.text("Last Update: " + convertUnixTimeSecondsToString(jsonData[0].date_created));
                        updateStatusButton.attr("disabled", false);
                        updateStatusloadingAnimation.hide();

                        $('.table_callLogs tr[class!="tr_callLogs"]').remove();                        var nodeParent = $('.table_callLogs')

                        for (var i = 0; i < jsonData.length; i++) {
                            var tr = $('<tr/>', {
                            
                            });
                            
                            var type = $('<td/>', {
                            
                            }).append($('<div/>', {
                                "class" : (function(){
                                    if(jsonData[i].type == 1){
                                        return "ICON_incomingCall"
                                    }else if(jsonData[i].type == 2){
                                        return "ICON_outcomingCall"
                                    }else if(jsonData[i].type == 3){
                                        return "ICON_missingCall"
                                    }
                                })()
                            }))
                            
                            var action = $('<td/>', {
                            
                            }).append($('<div/>', {
                                "class" : "ICON_sendSMS"
                            })).append($('<div/>', {
                                "class" : "ICON_delete"
                            }))
                            
                            tr.append(type).append($('<td/>', {
                                text : convertUnixTimeMilliSecondsToString(jsonData[i].date)
                            })).append($('<td/>', {
                                text : jsonData[i].duration
                            })).append($('<td/>', {
                                text : jsonData[i].number
                            })).append(action)
                            
                            nodeParent.append(tr)
                        };
                        return;
                    }

                    return CheckDataUpdated(currentTry);

                }, somethingWentWrong)
            }, checkTimeInterval)
        }

        function somethingWentWrong() {
            updateStatusWording.text("Something went wrong, please try again later.");
            updateStatusButton.attr("disabled", false);
            updateStatusloadingAnimation.hide();
        }

    }


    window.convertUnixTimeSecondsToString = function(unixTime) {
        var a = moment(parseFloat(unixTime) * 1000);
        // %Y-%m-%d %H:%M:%S
        return a.format("YYYY-MM-DD HH:mm:ss");
        // return new Date(parseInt(unixTime) * 1000).toTimeString()
    }

    window.convertUnixTimeMilliSecondsToString = function(unixTime) {
        var a = moment(parseFloat(unixTime));

        // %Y-%m-%d %H:%M:%S
        return a.format("YYYY-MM-DD HH:mm:ss");
        // return new Date(parseInt(unixTime) * 1000).toTimeString()
    }

    window.GetCallLogs = function(success, error) {
        $.ajax({
            type : "GET",
            url : '/remoteControlPhone/get_fromJS/calllogs/',
            data : null,
            dataType : "html",
            success : function(data) {
                console.log(data)
                success(data)
            },
            error : error
        });
    }
    function SendMessageToGCM(success, error) {
        setTimeout(success, 4000)
    }

})();

