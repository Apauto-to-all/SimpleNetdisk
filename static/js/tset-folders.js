async function getFolders(parentFolderId = 'root') {
    if (parentFolderId == "root") {
        return { '/': '根目录' };
    }
    try {
        const response = await fetch(`/getfolders?parent_folder_id=${parentFolderId}`, {
            method: 'GET',
            // 需要添加适当的headers，例如用于认证的Cookie
        });
        const folders = await response.json();
        if (response.ok) {
            return folders;
        } else {
            throw new Error('Failed to fetch folders');
        }
    } catch (error) {
        console.error('Error fetching folders:', error);
        return {};
    }
}

async function buildFileTree(parentFolderId, parentElement, level = 0) {
    const folders = await getFolders(parentFolderId);
    if (Object.keys(folders).length === 0) {
        // 检查是否已经存在"无文件夹"提示
        let noFolderMsg = parentElement.querySelector('.no-folder-msg');
        if (!noFolderMsg) {
            noFolderMsg = document.createElement('div');
            noFolderMsg.className = 'no-folder-msg'; // 添加一个类名以便于识别
            noFolderMsg.textContent = '无文件夹';
            parentElement.appendChild(noFolderMsg);
        }
    } else {
        Object.entries(folders).forEach(([uuid, folderName]) => {
            // 创建文件夹元素
            const folderElement = document.createElement('div');
            folderElement.className = 'folder';
            folderElement.style.marginLeft = `${level * 20}px`;

            // 创建toggleButton元素
            const toggleButton = document.createElement('span');
            toggleButton.className = 'toggle';
            toggleButton.textContent = '+';
            toggleButton.onclick = function (event) {
                event.stopPropagation(); // 防止事件冒泡
                if (toggleButton.textContent === '+') {
                    // 展开子文件夹
                    buildFileTree(uuid, folderElement, level + 1).then(() => {
                        toggleButton.textContent = '-';
                    });
                } else {
                    // 收起子文件夹
                    const childFolders = folderElement.querySelectorAll('.folder');
                    childFolders.forEach(child => {
                        if (child.style.marginLeft > folderElement.style.marginLeft) {
                            folderElement.removeChild(child);
                        }
                    });
                    // 移除"无文件夹"提示，如果有的话
                    const noFolderMsg = folderElement.querySelector('.no-folder-msg');
                    if (noFolderMsg) {
                        folderElement.removeChild(noFolderMsg);
                    }
                    toggleButton.textContent = '+';
                }
            };
            // 定义一个函数来获取特定cookie的值
            function getCookie(name) {
                let cookieArray = document.cookie.split('; ');
                for (let cookie of cookieArray) {
                    let [cookieName, cookieValue] = cookie.split('=');
                    if (cookieName === name) {
                        var cp_or_move = decodeURIComponent(cookieValue);
                        if (cp_or_move == 'True') {
                            return true;
                        } else if (cp_or_move == 'False') {
                            return false;
                        } else {
                            return null;
                        }
                    }
                }
                return null;
            }
            // 创建按钮元素，移动或复制
            var is_cp_or_move = getCookie('cp_or_move');// 移动为false，复制为true
            // 创建操作按钮
            const actionButton = document.createElement('button');
            actionButton.id = uuid;
            if (is_cp_or_move == false) {
                actionButton.textContent = '移动到此文件夹';
            }
            else if (is_cp_or_move == true) {
                actionButton.textContent = '复制到此文件夹';
            } else {
                actionButton.textContent = '未知操作';
            }
            // 为按钮添加点击事件处理函数
            actionButton.onclick = function () {
                // 在这里添加移动或复制文件到文件夹的逻辑
                if (is_cp_or_move != null) {
                    // 移动文件
                    if (is_cp_or_move == false) {
                        fetch(`/move_to_folder?target_folder_id=${uuid}`, {
                            method: 'GET',
                            credentials: 'include', // 确保cookies被发送
                        }).then(response => {
                            if (response.redirected) {
                                window.location.href = response.url; // 如果有重定向，跟随到新的URL
                                return;
                            } else {
                                response.json().then(data => {
                                    if (data.error) {
                                        alert(data.error);
                                    }
                                });
                            }
                        }).catch(error => console.error('Error:', error));
                    }
                    // 复制文件
                    else if (is_cp_or_move == true) {
                        fetch(`/copy_to_folder?target_folder_id=${uuid}`, {
                            method: 'GET',
                            credentials: 'include', // 确保cookies被发送
                        }).then(response => {
                            if (response.redirected) {
                                window.location.href = response.url; // 如果有重定向，跟随到新的URL
                                return;
                            } else {
                                response.json().then(data => {
                                    if (data.error) {
                                        alert(data.error);
                                    }
                                });
                            }
                        }).catch(error => console.error('Error:', error));
                    }
                }
            };

            // 创建图标元素
            const iconElement = document.createElement('span');
            iconElement.className = 'icon';
            // 创建文件夹名称元素
            const folderNameElement = document.createElement('span');
            folderNameElement.textContent = ` ${folderName}`;
            // 将元素添加到folderElement中
            folderElement.appendChild(toggleButton);
            folderElement.appendChild(iconElement); // 将图标元素添加到folderElement中，紧跟在toggleButton之后
            folderElement.appendChild(folderNameElement);
            folderElement.appendChild(actionButton); // 将按钮元素添加到folderElement中，紧跟在folderNameElement之后

            parentElement.appendChild(folderElement);
        });
    }
}

window.onload = function () {
    const fileTreeRoot = document.getElementById('file-tree');
    buildFileTree('root', fileTreeRoot);
};