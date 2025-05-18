# class2 _类二_

多进程对大模型合成的音频文件计算声音特征；比较不同文字和角色的声音特征有无区别（进程池/进程执行器实现管理）

```python
import librosa
import matplotlib.pyplot as plt
from multiprocessing import Process
from multiprocessing import Pool
from multiprocessing import current_process
import numpy as np
import os
import math

class MultiProcessVoiceFeature:
    def __init__(self, dirpath, num_process, savepath):
        self.dirpath = dirpath
        self.num_process = num_process
        self.savepath = savepath
```

类中初始化方法，传入参数：类一中处理后的八个音频文件路径，进程数，保存路径

---

1. 比较语速，根据每个块中的文件挨个处理并保存结果到一个元组，加入到一个列表中，返回列表

```python
    def _diff_speed(self, file_lst):
        results=[]
        for file in file_lst:
            file_path=os.path.join(self.dirpath,file)
            fname=os.path.splitext(file)[0]
            
            y, sr=librosa.load(file_path, sr=None)
            
            onsets = librosa.onset.onset_detect(y=y,sr=sr,units="time",hop_length=128,
                                                backtrack=False)
            num_words=len(onsets)
            duration=len(y)/sr
            
            speed=num_words/duration
        
            results.append((fname, num_words,duration,speed))
          
        return results
```

2. 比较音高，绘制每个文件的音高的图，保存；传入参数：处理的块

```python
    def _diff_pitch(self, file_lst):
        for file in file_lst:
            fname=str(os.path.splitext(file)[0])
            file_path=os.path.join(self.dirpath,file)
            
            y, sr=librosa.load(file_path, sr=None)
            pitch = librosa.yin(y,fmin=librosa.note_to_hz('C1'),
                                fmax=librosa.note_to_hz('C7'))
            times = librosa.times_like(pitch, sr=sr)
            
            #画布
            plt.plot(times,pitch)
            title=fname+' pitch'+'.png'
            save_path = os.path.join(self.savepath,title)
            plt.title(fname+' pitch')
            
            plt.savefig(save_path,dpi=300,bbox_inches = 'tight')
            print(title,' is saved!')
```

3. 比较声强，绘制每个文件的声压图，保存；传入参数：处理的块

```python
        
    def _diff_sdb(self,file_lst):
        for file in file_lst:
            fname=str(os.path.splitext(file)[0])
            file_path=os.path.join(self.dirpath,file)
        
            y, sr = librosa.load(file_path, sr=None)
            sdb=librosa.amplitude_to_db(librosa.feature.rms(y=y).squeeze(),
                                        ref=0.00002)
            
            times = librosa.frames_to_time(np.arange(len(sdb)), sr=sr)
            
            # 画图
            fig, axes = plt.subplots(1,2,figsize=(10,8),sharex=True)
            librosa.display.waveshow(y=y, sr=sr, ax=axes[0]) # 波形图
            axes[0].set_title('sdb wave for {}'.format(fname))
            axes[0].set_ylabel('Amplitude')
            axes[1].plot(times, sdb, color='blue', alpha=0.8) # 声压
            axes[1].set_title('sdb wave for {}'.format(fname))
            axes[1].set_ylabel('dB Level')
            
            title=fname+' in sdb'
            fig.suptitle(title)
            title=title+'.png'
            save_path = os.path.join(self.savepath,title)
            fig.savefig(save_path,dpi=300,bbox_inches = 'tight')
            print(title,'is saved!')
```

4. 分割文件夹的函数，进行列表操作

```python
    def _slice_file(self):
        dirpath = self.dirpath
        d = [f for f in os.listdir(dirpath) if f.endswith('.mp3')]
        chunk_size = math.ceil(len(d)/self.num_process)
        start=0
        reminder=len(d)%self.num_process
        sliced_lst=[]
        for i in range(self.num_process):
            end=start+chunk_size+(1 if i<reminder else 0)
            sliced_lst.append(d[start:end])
            start=end
        return sliced_lst
```

5. 主函数，传入参数：用户模式（1：声高，2：声压，3：语速）

```python
    def multiProcess(self, user_mode):
        sliced_lst=self._slice_file()
        pool=Pool(processes=self.num_process)
        processes = []
        if user_mode == 1:
            func=self._diff_pitch
            print('user mode: pitch')
        elif user_mode == 2:
            func=self._diff_sdb
            print('user mode: sdb')
        elif user_mode == 3:
            func=self._diff_speed
            print('user mode: speed')
        else:
            print('plz put in standard string!')
        
        for slice_piece in sliced_lst:
            proc = pool.apply_async(func, args=(slice_piece,))
            processes.append(proc)
        pool.close()
        pool.join()
        results=[]
        for process in processes:
            results.append(process.get())
        for result in results:
            if result:
                print(result)
```

只能在__main__中运行，否则会报错;**用户模式（1：声高，2：声压，3：语速）**

```python

if __name__=='__main__':
    #dirpath, num_process, savepath
    savepath='/Users/wtsama/Documents/code/'
    dirpath='/Users/wtsama/Documents/code/python文件大型/week12/syzed_voice/'
    num_process=2
    user_modes=[1,2,3]
    class2=MultiProcessVoiceFeature(dirpath,num_process,savepath)
    print('Start loading...')
    for user_mode in user_modes:
        class2.multiProcess(user_mode=user_mode)
    print('Bye!')

```
