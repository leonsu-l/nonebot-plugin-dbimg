<?php
$REPO_PATH = "/path/to/your/repo";

chdir($REPO_PATH);

exec('git pull 2>&1', $output, $exitCode);

if ($exitCode !== 0) {
    http_response_code(500);
} else {
    exec('nb stop', $output, $exitCode);
    exec('nb run', $output, $exitCode);
    http_response_code(200);
}
