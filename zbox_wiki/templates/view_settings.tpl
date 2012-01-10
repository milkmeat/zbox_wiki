$def with (show_full_path, auto_toc, highlight, static_files)
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>View Settings</title>

    <style>
        #new_path { width : 400px; }
    </style>

    $if static_files:
        $static_files

</head>
<body>


<div id="container">

    <h1>View Settings</h1>

    <div id="view-settings">
        <form method="POST">


            <label for="show_full_path">show full path</label>

            $if show_full_path:
                <input type="checkbox" id="show_full_path" name="show_full_path" checked="checked" />
            $else:
                <input type="checkbox" id="show_full_path" name="show_full_path" />
            <br />


            <label for="auto_toc">auto <b>T</b>able <b>O</b>f <b>C</b>ontent</label>

            $if auto_toc:
                <input type="checkbox" id="auto_toc" name="auto_toc" checked="checked" />
            $else:
                <input type="checkbox" id="auto_toc" name="auto_toc" />
            <br />


            <label for="highlight">highlight source code</label>

            $if highlight:
                <input type="checkbox" id="highlight" name="highlight" checked="checked" />
            $else:
                <input type="checkbox" id="highlight" name="highlight" />
            <br />



            <div id="toolbox">
                <input type="submit" value="Rename" />
            </div>
        </form>
    </div>

</div>


</body>
</html>