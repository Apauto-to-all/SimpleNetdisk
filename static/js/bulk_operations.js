// 批量下载
async function downloadALL() {
    var checkboxes = document.querySelectorAll('input[type=checkbox].file:checked');
    for (var i = 0; i < checkboxes.length; i++) {
        // 创建新的 a 元素
        var link = document.createElement('a');
        link.href = '/download?file_id=' + checkboxes[i].id;
        link.download = 'file_' + checkboxes[i].id;  // 设置下载的文件名
        link.style.display = 'none';  // 隐藏元素
        document.body.appendChild(link);  // 将元素添加到页面中
        link.click();  // 模拟点击元素
        document.body.removeChild(link);  // 从页面中移除元素

        // 等待一段时间以允许文件下载开始
        await new Promise(resolve => setTimeout(resolve, 100));

    }
}
// 批量删除
async function deleteAll() {
    var checkboxesFile = document.querySelectorAll('input[type=checkbox].file:checked');
    var checkboxesFolder = document.querySelectorAll('input[type=checkbox].folder:checked');
    if (checkboxesFile.length + checkboxesFolder.length === 0) {
        alert('请至少选择一个文件或文件夹');
        return;
    }
    var promises = [];
    for (var i = 0; i < checkboxesFile.length; i++) {
        // 批量删除，发送get请求
        var promise = await fetch('/delete?file_id=' + checkboxesFile[i].id, { method: 'GET', credentials: 'include' });
        promises.push(promise);
    }
    for (var i = 0; i < checkboxesFolder.length; i++) {
        // 批量删除，发送get请求
        var promise = await fetch('/delete?folder_id=' + checkboxesFolder[i].id, { method: 'GET', credentials: 'include' });
        promises.push(promise);
    }
    if (promises.length === 0) {
        alert('请至少选择一个文件或文件夹');
        return;
    }
    Promise.all(promises).then(() => location.reload());
}

// 批量移动，设置cp_or_move的cookie，移动为False，复制为True
async function moveALL() {
    var folders_id = [];
    var files_id = [];
    var checkboxes = document.querySelectorAll('input[type=checkbox].file:checked');
    for (var i = 0; i < checkboxes.length; i++) {
        files_id.push(checkboxes[i].id);
    }
    checkboxes = document.querySelectorAll('input[type=checkbox].folder:checked');
    for (var i = 0; i < checkboxes.length; i++) {
        folders_id.push(checkboxes[i].id);
    }
    if (folders_id.length + files_id.length === 0) {
        alert('请至少选择一个文件或文件夹');
        return;
    }
    // 将数据储存到cookie，key=files_id, value=files_id（列表），key=folders_id, value=folders_id（列表）
    document.cookie = 'files_id=' + JSON.stringify(files_id) + '; path=/';
    document.cookie = 'folders_id=' + JSON.stringify(folders_id) + '; path=/';
    // 跳转到文件树页面
    fetch('/set_cookie_move', {
        method: 'GET',
        credentials: 'include', // 确保cookies被发送
    }).then(response => {
        if (response.redirected) {
            window.location.href = response.url; // 如果有重定向，跟随到新的URL
        }
    }).catch(error => console.error('Error:', error));
}

// 批量复制，设置cp_or_move的cookie，移动为False，复制为True
async function copyALL() {
    var folders_id = [];
    var files_id = [];
    var checkboxes = document.querySelectorAll('input[type=checkbox].file:checked');
    for (var i = 0; i < checkboxes.length; i++) {
        files_id.push(checkboxes[i].id);
    }
    checkboxes = document.querySelectorAll('input[type=checkbox].folder:checked');
    for (var i = 0; i < checkboxes.length; i++) {
        folders_id.push(checkboxes[i].id);
    }
    if (folders_id.length + files_id.length === 0) {
        alert('请至少选择一个文件或文件夹');
        return;
    }
    // 将数据储存到cookie，key=files_id, value=files_id（列表），key=folders_id, value=folders_id（列表）
    document.cookie = 'files_id=' + JSON.stringify(files_id) + '; path=/';
    document.cookie = 'folders_id=' + JSON.stringify(folders_id) + '; path=/';
    // 跳转到文件树页面
    fetch('/set_cookie_cp', {
        method: 'GET',
        credentials: 'include', // 确保cookies被发送
    }).then(response => {
        if (response.redirected) {
            window.location.href = response.url; // 如果有重定向，跟随到新的URL
        }
    }).catch(error => console.error('Error:', error));
}