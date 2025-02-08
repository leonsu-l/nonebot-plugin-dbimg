<?php
$REPO_PATH = "/path/to/your/repo";
$UUID = "";
$DAEMON_ID = "";
$APIKEY = "";
$SERVER_IP_AND_PORT = "";

chdir($REPO_PATH);

exec('git pull 2>&1', $output, $exitCode);

if ($exitCode !== 0) {
    http_response_code(500);
} else {
    $url = "http://" . $SERVER_IP_AND_PORT . "/api/protected_instance/restart?uuid=" . urlencode($UUID) . "&daemonId=" . $DAEMON_ID . "&apikey=" . urlencode($APIKEY);

    // 初始化cURL会话
    $ch = curl_init();

    // 设置cURL选项
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Content-Type: application/json; charset=utf-8',
        'X-Requested-With: XMLHttpRequest'
    ]);

    // 执行cURL请求
    $response = curl_exec($ch);

    // 检查是否有错误发生
    if (curl_errno($ch)) {
        http_response_code(500);
    } else {
        http_response_code(200);
    }

    // 关闭cURL会话
    curl_close($ch);
}
