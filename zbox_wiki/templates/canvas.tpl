$def with (conf, req_path, title, content, static_files=None, toolbox=True, quicklinks=True)
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>$req_path</title>

    $if static_files:
        $static_files

</head>
<body>


<div id="container">

$if quicklinks:
    <div id="quicklinks">
        <a href="/home">Home</a>
        <a href="/~recent-changes">Recent Changes</a>
        <a href="/~all">All</a>
        <a href="/~settings">Settings</a>
    </div>

    <div id="searchbox">
        <form method="POST" action="/~search" accept-charset="utf-8">
            <input type="text" name="k" class="auto-increase-width-size" />
            <input type="submit" value="Search" />
        </form>
    </div>


<div id="title">$title</div>

<div id="content">$content</div>


$if toolbox:
    <div id="toolbox">
        <a href="/$req_path?action=source">Source</a>

        $if not conf.readonly:
            <a href="/$req_path?action=delete">Delete</a>
            <a href="/$req_path?action=rename">Rename</a>
            <a href="/$req_path?action=edit">Edit</a>

    </div>


</div>


$if conf.readonly and conf.maintainer_email:
    $ email = conf.maintainer_email_prefix + '<span class="hide">null</span>@' + conf.maintainer_email_suffix
    <footer>
        <p>
            Maintainer: $email
        </p>
    </footer>

</body>
</html>
