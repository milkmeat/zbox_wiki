$def with (conf, button_path = None, content = "", req_path = None, static_files = None, show_quick_links = True, paginator = None, show_source_button = True)
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title></title>

    <link rel="shortcut icon" href="/static/favicon.ico" />

    $if static_files:
        $static_files

</head>
<body>


<div id="container">


<div id="quick_links">
    <a href="/">Home</a>

    $if show_quick_links:
        <a href="/~recent">Recent Changes</a>
        <a href="/~all">All</a>
        <a href="/~settings">Settings</a>
</div>

$if show_quick_links:
    <div id="searchbox">
        <form method="POST" action="/~search" accept-charset="utf-8">
            <input type="text" name="k" class="auto-increase-width-size" />
            <input type="submit" value="Search" />
        </form>
    </div>


$if button_path:
    <div id="button_path">$button_path</div>


$if paginator:
    $if paginator.has_previous_page:
        <div id="previous_page_btn"><a href="$paginator.previous_page_url">previous</a></div>

    $if paginator.has_next_page:
        <div id="next_page_btn"><a href="$paginator.next_page_url">next</a></div>


<div id="content">$content</div>


$if req_path:
    <div id="toolbox">
        $if show_source_button:
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
