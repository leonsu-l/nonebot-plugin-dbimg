<?php
$REPO_PATH = "/path/to/your/repo";

chdir($REPO_PATH);

exec('git pull 2>&1', $output, $exitCode);

$output = implode("\n", $output);

if ($exitCode !== 0) {
    http_response_code(500);
    echo "<pre>Failed to pull repository:\n$output</pre>";
} else {
    http_response_code(200);
    echo "<pre>Repository updated successfully:\n$output</pre>";
}
