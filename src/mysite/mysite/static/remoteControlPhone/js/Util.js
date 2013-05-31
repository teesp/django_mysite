(function() {
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

})();

