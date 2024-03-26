<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Realtime and Past Data Viewer</title>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <style>
        .tab {
            overflow: hidden;
            border: 1px solid #ccc;
            background-color: #f1f1f1;
        }

        .tab button {
            background-color: inherit;
            float: left;
            border: none;
            outline: none;
            cursor: pointer;
            padding: 14px 16px;
            transition: 0.3s;
        }

        .tab button:hover {
            background-color: #ddd;
        }

        .tab button.active {
            background-color: #ccc;
        }

        .tabcontent {
            display: none;
            padding: 6px 12px;
            border: 1px solid #ccc;
            border-top: none;
        }
    </style>
</head>
<body>
<div class="tab">
    <button class="tablinks" onclick="openTab(event, 'realtime')">Realtime Data</button>
    <button class="tablinks" onclick="openTab(event, 'past')">Past Data</button>
</div>

<div id="realtime" class="tabcontent">
    <h3>Realtime Data</h3>
    <div id="realtimeData"></div>
</div>

<div id="past" class="tabcontent">
    <h3>Past Data</h3>
    <div id="pastData"></div>
</div>

<script>
    function openTab(evt, tabName) {
        var i, tabcontent, tablinks;
        tabcontent = document.getElementsByClassName("tabcontent");
        for (i = 0; i < tabcontent.length; i++) {
            tabcontent[i].style.display = "none";
        }
        tablinks = document.getElementsByClassName("tablinks");
        for (i = 0; i < tablinks.length; i++) {
            tablinks[i].className = tablinks[i].className.replace(" active", "");
        }
        document.getElementById(tabName).style.display = "block";
        evt.currentTarget.className += " active";
    }

    function fetchRealtimeData() {
        $.get('https://siddhi-project-67c6e-default-rtdb.firebaseio.com/realtime.json', function (data) {
            var html = '';
            if (data) {
                var keys = Object.keys(data);
                var latestData = data[keys[keys.length - 1]]; // Get the latest data
                html += '<pre>' + JSON.stringify(latestData, null, 2) + '</pre>';
            } else {
                html += '<p>No data available</p>';
            }
            $('#realtimeData').html(html);
        });
    }

    function fetchPastData() {
    $.get('https://siddhi-project-67c6e-default-rtdb.firebaseio.com/past.json', function (data) {
        var html = '';
        if (data) {
            // Display past data here
            html += '<table>';
            for (var key in data) {
                html += '<tr>';
                for (var subKey in data[key]) {
                    html += '<td>' + data[key][subKey] + '</td>';
                }
                html += '</tr>';
            }
            html += '</table>';
        } else {
            html += '<p>No data available</p>';
        }
        $('#pastData').html(html);
    });
}

    function refreshRealtimeData() {
        fetchRealtimeData();
        setTimeout(refreshRealtimeData, 5000); // Refresh every 5 seconds
    }

    function refreshPasttimeData() {
        fetchPastData();
        setTimeout(refreshPasttimeData, 5000); // Refresh every 5 seconds
    }
    // Initial fetch and refresh for real-time data
    fetchRealtimeData();
    refreshRealtimeData();
    refreshPasttimeData();

    // Initial fetch for past data
    fetchPastData();
</script>
</body>
</html>
