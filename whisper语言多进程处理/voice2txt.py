import sys
import whisper
from multiprocessing import Process # 标准库中用于创建子进程的类，不用自己写
import zipfile
import os
from pathlib import Path
import warnings

# 忽略特定的 UserWarning
warnings.filterwarnings("ignore", category=UserWarning, message="FP16 is not supported on CPU")

#whisper_model=whisper.load_model('medium') # 多进程中，每个进程都有独立的内存空间。如果在主进程加载模型，子进程无法直接共享该模型实例，会导致模型被重复加载到每个子进程的内存中。

#解压文件的函数，放在主进程中
def unzip(path,extract_path):
    with zipfile.ZipFile(path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    print('解压完成，解压到{}'.format(extract_path))
    return

#=====================================================================================================================================
# 子进程，分为 -加载模型的函数process_lst 和-转化单个文件的函数voice2test
# 子进程一
def process_lst(start, end, clip_lst, text_dir):
    '''
    每个chunk里面加载模型
    '''
    print(f'Process {os.getpid()} 加载模型中...')
    try:
        model = whisper.load_model('medium')                        # medium模型；  模型加载应该放在每个chunk前面分别加载，每个子进程独立加载模型，避免主进程与子进程间的内存冲突；同时每个子进程的文件共享一个模型加载，避免开销
        for j in range(start, end+1):
            voice2text(model, clip_lst[j-1], text_dir, j)
    except Exception as e:
        print(f'进程错误: {str(e)}')
# 子进程二
def voice2text(model, file, text_dir, work_id):
    '''
    转化单个文件
    '''
    print(f'Work ID {work_id} processing file: {file}')             # 打印文件路径确认
    try:
        # 确保文件存在
        if not os.path.exists(file):
            raise FileNotFoundError(f"Audio file not found: {file}")
            
        result = model.transcribe(file, verbose=False)
        text = result['text']
        
        # 确保输出目录存在
        os.makedirs(text_dir, exist_ok=True)
        
        output_path = os.path.join(text_dir, f'{work_id}.txt')
        with open(output_path, 'w', encoding='utf-8') as text_file:
            text_file.write(text)
        print(f'{file} 转录完成! 结果保存到 {output_path}')
    except Exception as e:
        print(f'处理文件 {file} 时出错: {str(e)}')


# %%
# 间接用子进程
class Task(Process):

    def __init__(self):
        super.__init__()
        
    def process_lst(self, start, end, clip_lst, text_dir):
        '''
        每个chunk里面加载模型
        '''
        print(f'Process {os.getpid()} 加载模型中...')
        try:
            model = whisper.load_model('medium')                        # medium模型；  模型加载应该放在每个chunk前面分别加载，每个子进程独立加载模型，避免主进程与子进程间的内存冲突；同时每个子进程的文件共享一个模型加载，避免开销
            for j in range(start, end+1):
                self._voice2text(model, clip_lst[j-1], text_dir, j)
        except Exception as e:
            print(f'进程错误: {str(e)}')
            
    def _voice2text(self, model, file, text_dir, work_id):
        '''
        转化单个文件
        '''
        print(f'Work ID {work_id} processing file: {file}')             # 打印文件路径确认
        try:
            # 确保文件存在
            if not os.path.exists(file):
                raise FileNotFoundError(f"Audio file not found: {file}")
                
            result = model.transcribe(file, verbose=False)
            text = result['text']
            
            # 确保输出目录存在
            os.makedirs(text_dir, exist_ok=True)
            
            output_path = os.path.join(text_dir, f'{work_id}.txt')
            with open(output_path, 'w', encoding='utf-8') as text_file:
                text_file.write(text)
            print(f'{file} 转录完成! 结果保存到 {output_path}')
        except Exception as e:
            print(f'处理文件 {file} 时出错: {str(e)}')

# %%
    
#=================================================================================================================================
#主进程读取声音数据（见live_voice.zip)，得到所有声音文件的列表，并为子进程分发需要处理的文件；
if __name__=="__main__":
    audio_path="F:/github_repository/live_voice.zip"
    unzip_path="F:/github_repository/live_voice/"
    
    print('开始解压...')
    unzip(audio_path,unzip_path)

    print('文件已经解压，进入下一步操作...')
    #text path
    text_dir="F:/github_repository/voice2text/"
    

        
    dir_root=os.path.join(unzip_path,'voice/')

    for r, d, f in os.walk(dir_root):                                   # 找到根目录为止（root, dir, file)
        if len(d):                                                      # 文件夹非空
            dir=d # ['3509011980579168334_1646279051', '3508465183997701964_1646237867', ...]
            
    clip_lst=[]
    for i in dir:
        p= Path(os.path.join(dir_root,i))
        # ../live_voice/voice/3509011980579168334_1646279051...
        only_f=str(next(p.iterdir()))
        
        # ../live_voice/voice/3509011980579168334_1646279051/clip.mp3
        clip_lst.append(only_f)
    
    chunk_size=(len(clip_lst)+2-1)//2                                   # 向下取整
    processes=[]
    
    for i in range(2):
        start=i*chunk_size+1
        end=min((i+1)*chunk_size,len(clip_lst))
        if start>end: # start:1, end:5
            continue

#======================================================================================================================================
# 直接使用Process类构建子进程，利用whisper库将音频数据转成文本数据，并将结果保存为文件（一个音频文件对应一个文本文件 ）。
#        proc=Process(target=process_lst,
#                        args=(start, end, clip_lst, text_dir))
#======================================================================================================================================
# 通过继承Process类来构建子进程，同样利用whisper库将音频数据转成文本数据，并将结果保存为文件（一个音频文件对应一个文本文件 ）。
        Proc = Task()
        proc = Proc.process_lst(start, end, clip_lst, text_dir)
        
        proc.start()
        processes.append(proc)
    for proc_i in processes:
        proc_i.join()
        
    print('main')
    
    


    
