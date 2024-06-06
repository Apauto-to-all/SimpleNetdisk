// 垃圾桶页面的js
// 全选检测，全选或全不选
function chk_all() {
    var chkall = document.getElementById('chkall').checked;
    var checkboxes = document.querySelectorAll('input[type=checkbox]');
    for (var i = 0; i < checkboxes.length; i++) {
        checkboxes[i].checked = chkall;
    }
}
// 单选检测，全选或部分选中
function chk_single() {
    var checkboxes = document.querySelectorAll('input[type=checkbox].checkboxItem');
    var allChecked = true;
    var someChecked = false;
    for (var i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked) {
            someChecked = true;
        } else {
            allChecked = false;
        }
    }
    var chkall = document.getElementById('chkall');
    chkall.checked = allChecked;
    chkall.indeterminate = someChecked && !allChecked;
}
// 还原文件夹或文件
function restore() {
    // 获取所有选中的文件夹和文件
    var folders = [];
    var files = [];
    var checkboxes = document.querySelectorAll('input[type=checkbox].checkboxItem');
    for (var i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked) {
            if (checkboxes[i].className.includes('folder')) {
                folders.push(checkboxes[i].id);
            }
            if (checkboxes[i].className.includes('file')) {
                files.push(checkboxes[i].id);
            }
        }
    }
    // 发送请求还原文件夹和文件
    fetch('/restore', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            folders: folders,
            files: files
        })
    })
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                window.location.reload();
            } else if (result.error) {
                alert(result.error); // 如果有错误信息，显示错误信息
            } else {
                alert('还原失败，未知错误'); // 其他情况，显示未知错误
            }
        })
        .catch(error => console.error('Error:', error));
}
// 永久删除文件夹或文件
function deleteForever() {
    // 获取所有选中的文件夹和文件
    var folders = [];
    var files = [];
    var checkboxes = document.querySelectorAll('input[type=checkbox].checkboxItem');
    for (var i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked) {
            if (checkboxes[i].className.includes('folder')) {
                folders.push(checkboxes[i].id);
            }
            if (checkboxes[i].className.includes('file')) {
                files.push(checkboxes[i].id);
            }
        }
    }
    // 发送请求永久删除文件夹和文件
    fetch('/delete_forever', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            folders: folders,
            files: files
        })
    })
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                window.location.reload();
            } else if (result.error) {
                alert(result.error); // 如果有错误信息，显示错误信息
            } else {
                alert('删除失败，未知错误'); // 其他情况，显示未知错误
            }
        })
        .catch(error => console.error('Error:', error));
}
// 获取用户名
fetch('/get_username', {
    method: 'GET',
})
    .then(response => response.text())  // 将响应转换为文本
    .then(username => {
        document.getElementById('username').textContent = username;
    })
    .catch(error => console.error('Error:', error));

// 获取回收站文件夹和文件
fetch('/trash/folder', {
    method: 'GET',
    credentials: 'include'  // 需要这个选项来发送和接收cookies
})
    .then(response => response.json())  // 将响应转换为JSON
    .then(folders => {
        const foldersElement = document.getElementById('folders');
        folders.forEach(folder => {
            const li = document.createElement('li');

            // 添加缩略图
            const img = document.createElement('img'); // 创建一个img元素
            img.src = '/thumbnail/folder'

            // 创建复选框
            const checkbox = document.createElement('input'); // 创建一个input元素
            checkbox.type = 'checkbox'; // 设置复选框类型
            checkbox.id = `${folder.uuid}`;  // 假设每个文件夹有一个唯一的ID
            checkbox.className = 'folder checkboxItem'; // 添加class属性
            checkbox.onclick = chk_single; // 点击复选框时触发chk_single函数

            // 创建文本节点
            const text = document.createTextNode(` 文件夹名: ${folder.folder_name}, 放入回收站时间: ${folder.drop_time}, 删除时间: ${folder.delete_time}`);

            // 将复选框和文本节点添加到li元素
            li.appendChild(checkbox);
            li.appendChild(img)
            li.appendChild(text);

            foldersElement.appendChild(li);
        });
    })
    .catch(error => console.error('Error:', error));



// 获取回收站文件
fetch('/trash/file', {
    method: 'GET',
    credentials: 'include'  // 需要这个选项来发送和接收cookies
})
    .then(response => response.json())  // 将响应转换为JSON
    .then(files => {
        const filesElement = document.getElementById('files');
        files.forEach(file => {
            const li = document.createElement('li');

            // 添加缩略图/thumbnail/{file_type}
            const img = document.createElement('img'); // 创建一个img元素
            img.src = '/thumbnail/default'

            // 创建复选框
            const checkbox = document.createElement('input'); // 创建一个input元素
            checkbox.type = 'checkbox'; // 设置复选框类型
            checkbox.id = `${file.uuid}`;  // 假设每个文件有一个唯一的ID
            checkbox.className = 'file checkboxItem'; // 添加class属性
            checkbox.onclick = chk_single; // 点击复选框时触发chk_single函数

            // 创建文本节点
            const text = document.createTextNode(` 文件名: ${file.file_name}, 放入回收站时间: ${file.drop_time}, 删除时间: ${file.delete_time}`);

            // 将复选框和文本节点添加到li元素
            li.appendChild(checkbox);
            li.appendChild(img)
            li.appendChild(text);

            filesElement.appendChild(li);
        });
    })
    .catch(error => console.error('Error:', error));