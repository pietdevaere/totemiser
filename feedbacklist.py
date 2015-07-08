<!doctype html>
<html>
  <head>
    <title>Leddisplay -- Cycle</title>
    <style>
    table, th, td {
            border: 1px solid black;
    }
    </style>
  </head>
  <body>
    <div id="content">
        <h1>Leddisplay cycle configuration page</h1>
        <h2>Current configuration</h2>
        <table>
            <tr>
                <th>Index</th>
                <th>Type</th>
                <th>Content</th>
                <th>Row</th>
                <th>Update</th>
                <th>Extra Config</th>
                <th>Delete</th>
                <th>Move to</th>
            </tr>
            {% for effect in cycle.get_dict_array() %}
            <tr>
                <td>{{effect['index']}}</td>
                <td>{{effect['effect_type']}}</td>
                <td>{{effect['inner_content']}}</td>
                <td>{{effect['row']}}</td>
                <td>{{effect['update']}}</td>
                <td>{{effect['extra_config']}}</td>
                <td><form method="POST">
                    <input type="hidden" name="index" value="{{effect['index']}}">
                    <input type="submit" name="action" value="Delete">
                </form></td>
                <td><form method="POST">
                    <input type="hidden" name="index" value="{{effect['index']}}">
                    <input type="text" name="toIndex" class="indexField">
                    <input type="submit" name="action" value="Move">
                </form></td>
            </tr>
            {% endfor %}
        </table>
        
        <h2>Add new effects</h2>
        <h3>Static Row</h3>
        <form method='POST'>
            Index: <input type="text" name="index" value="999" class="indexField">
            Text: <input type="text" name="inner_content" value="Hello World">
            row:    <select name="row">
                        <option value="0">Bottom</option>
                        <option value="1">Top</option>
                    </select>
            Justify:    <select name="justify">
                        <option value="center">Center</option>
                        <option value="left">Left</option>
                    <!-- <option value="right">Right</option> -->
                    </select>
            Update: <input type="checkbox" name="update" value="update" checked="checked"> 
            <input type="hidden" name="type" value="static_row">
            <input type="submit" name="action" value="Create">
        </form>

        <h3>Static Display</h3>
        <form method='POST'>
            Index: <input type="text" name="index" value="999" class="indexField">
            Text: <input type="text" name="inner_content" value="Hello World">
            Update: <input type="checkbox" name="update" value="update" checked="checked"> 
            Justify:    <select name="justify">
                        <option value="center">Center</option>
                        <option value="left">Left</option>
                    <!-- <option value="right">Right</option> -->
                    </select>
            <input type="hidden" name="type" value="static_display">
            <input type="submit" name="action" value="Create">
        </form>

        <h3>Scolling Text</h3>
        <form method='POST'>
            Index: <input type="text" name="index" value="999" class="indexField">
            Text: <input type="text" name="inner_content" value="Hello World">
            Speed: <input type="text" name="speed" value="5">
            row:    <select name="row">
                        <option value="0">Bottom</option>
                        <option value="1">Top</option>
                    </select>
            <input type="hidden" name="type" value="scrolling_text">
            <input type="submit" name="action" value="Create">
        </form>

        <h2>Configuration options</h2>
        <h3>Save config</h3>
        <form method='POST'>
            Filename: <input type="text" name="filename" value="config">
            <input type="submit" name="action" value="Save">
        </form>

        <h3>Load config</h3>
        <form method='POST'>
            Filename: <select name="filename">
                        {% for filename in cycle.list_configs() %}
                        <option value="{{filename}}">{{filename}}</option>
                        {% endfor %}
                    </select>
            <input type="submit" name="action" value="Load">
        </form>

        <h3>Transfer to display</h3>
        <form method='POST'>
            <input type="submit" name="action" value="Transfer">
        </form>
    </div>
    <div id="footer">
      For support contact <a href="mailto:leddisplay@naas.be">leddisplay@naas.be</a>.
    </div>
  </body>
</html>
