# 前言

由于jupyternote book不能实现多进程处理大量文件，所以用python文件直接编译和实现。

# 运行环境

python3.12.2
依赖：openai-whisper==20240930
运行环境：windows11,cpu

# 双进程处理 20个mp3文件

文件位于解压后的live_voice.zip文件内，文件夹结构是

```plaintext
../live_voice/
        |__ /voice/
                 |__ 3509011980579168334_1646279051/
                                                   |__ clip.mp3
                 |__ xxxxxxxxxxxxxxxxxxx_xxxxxxxxxx/
                                                   |__ clip.mp3
                            ...(20个文件)

```

# 运行结果

总运行时间为 54min，将结果储存在text_dir="../voice2text/"中，有 20个txt文件