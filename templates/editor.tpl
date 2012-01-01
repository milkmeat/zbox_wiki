$def with (req_path, title, content, static_files=None)
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>Editing $req_path</title>

    $if static_files:
        $static_files


</head>
<body>


<div id="container">

<div id="editor">
    <form method="POST" accept-charset="utf-8">
        <div class="input-widget">
            <label for="content">Content</label>
            <textarea cols="80" rows="20" id="content" name="content">$content</textarea>
        </div>

        <div id="toolbox">
            <input type="submit" value="Update" />
        </div>

        <div class="help-links">
            <a href="http://daringfireball.net/projects/markdown/syntax" target="_blank">Markdown Syntax</a>, 
            <a href="http://daringfireball.net/projects/markdown/dingus" target="_blank">Markdown Dingus</a>
        </div>
    </form>
</div>

</div>


</body>
</html>