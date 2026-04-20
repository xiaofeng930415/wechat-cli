# WeChat CLI Code Wiki

`wechat-cli` 是一个用于解析和导出微信（macOS 版）本地聊天记录的命令行工具。

## 项目结构
- `bin/`: 存放命令行执行脚本。
- `commands/`: 包含所有支持的 CLI 命令（如 `history`, `export`, `search`, `stats` 等）。
- `core/`: 核心业务逻辑，包括数据库连接、消息查询、解密、类型解析。
  - `messages.py`: 处理消息记录查询、解析、媒体文件路径推断。
  - `contacts.py`: 处理联系人信息。
  - `decrypt.py`: 处理 SQLite 数据库的 SQLCipher 解密逻辑。
- `keys/`: 负责获取微信的加密密钥（通过内存搜索或 keychain）。
- `output/`: 控制终端文本和 JSON 格式的输出。

## 消息查询机制 (`wechat_cli/core/messages.py`)

1. **查询入口**: `collect_chat_history()` 会循环遍历消息数据库，执行 SQL 查询 `_query_messages()` 获取消息。
2. **格式化逻辑**: 每条记录通过 `_build_history_line()` 组装，并调用 `_format_message_text()` 解析正文。
3. **媒体路径解析**: 若使用 `--media` 参数，会调用 `_resolve_media_path()` 去推测对应的图片/文件位置。

### 媒体文件匹配缺陷 (Bug 分析)
工具在解析图片(`Type=3`)、视频(`Type=43`)或语音(`Type=34`)时，并没有真正从消息的 XML 中解析出文件名或哈希值，而是采用了一种非常粗暴的**目录枚举匹配**策略：

```python
# _resolve_media_path 中:
for d in search_dirs:
    sub = os.path.join(attach_dir, d, date_prefix, sub_dir_name)
    if os.path.isdir(sub):
        files = [f for f in os.listdir(sub) if not f.endswith("_h.dat")]
        if files:
            # 返回目录路径（具体是哪个文件无法从 XML 精确匹配）
            sample = files[0]
            return os.path.join(sub, sample), True
```

**这导致了一个严重的问题**：只要匹配到了 `YYYY-MM` 的对应聊天目录，它就会直接返回该目录下的**第一个文件** (`files[0]`)。因此，不论你在该月发了多少张图片，或者在同一秒内发了多少张图片，它查出来的图片路径永远是同一个（即 `os.listdir()` 返回的第一个文件）。

## 结论
该工具目前无法做到图片消息和物理文件的精确 1:1 映射。要修复此问题，需要解析 `Type=3` 消息的 XML（或根据 `msgId` 从其他表进行关联查询），获取真实的文件 MD5/文件名称，再拼接绝对路径。
