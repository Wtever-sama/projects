import librosa
import matplotlib.pyplot as plt
from multiprocessing import Process
from multiprocessing import Pool
from multiprocessing import current_process
import numpy as np
from itertools import combinations
import os
import math

class MultiProcessVoiceFeature:
    def __init__(self, dirpath, num_process, savepath):
        self.dirpath = dirpath
        self.num_process = num_process
        self.savepath = savepath
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
              