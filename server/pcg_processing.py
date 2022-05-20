from asyncio import streams
import pcg_matlab
import ffmpeg


class PcgProc():
    def __init__(self) -> None:
        self.matlab = pcg_matlab.initialize()

    def audio_info_mat(self, fn):
        " Информация о файле (matlab)"
        info, status = self.matlab.pcg_info(fn, nargout=2)
        if status == False:
            info = f'ERROR: {info}'
        return {'info': info, 'status': status}

    def audio_info_ff(self, fn):
        " Информация о файле (python)"
        try:
            info = ffmpeg.probe(fn)
            if (len(info) == 0) or (len(info.get('streams')) == 0) \
                    or (info['streams'][0]['codec_type'] != 'audio') \
                    or (info['streams'][0]['sample_rate'] == 0) \
                    or (info['streams'][0]['channels'] == 0) \
                    or (info['streams'][0].get('duration') is None):
                status = False
                info = 'ERROR: Unknow audio format.'
                return {'info': info, 'status': status}

            status = True
            i = {}
            i['CompressionMethod'] = info['streams'][0]['codec_name']
            i['NumChannels'] = info['streams'][0]['channels']
            i['SampleRate'] = info['streams'][0]['sample_rate']
            i['TotalSamples'] = float(
                info['streams'][0]['duration'])*int(info['streams'][0]['sample_rate'])
            i['Duration'] = info['streams'][0]['duration']
            info = i
        except Exception as e:
            status = False
            # info = str(e)
            info = 'ERROR: Read file error.'
        return {'info': info, 'status': status}

    def audio_info(self, fn):
        # return self.audio_info_ff(fn)
        return self.audio_info_mat(fn)

    def waveform(self, fn):
        fn_out = self.matlab.pcg_waveform(fn, nargout=1)
        return {'t': 'photo', 'v': fn_out}

################################################################################
# PROCESSING
################################################################################
    def processing(self, fn, redis):
        i = self.audio_info(fn)

        if i['status'] == False:
            yield {'t': 'text', 'v': i['info']}
            return
        #-------------------------------------------------------------------------
        compress = i['info']['CompressionMethod']
        channels = int(i['info']['NumChannels'])
        samplerate = int(i['info']['SampleRate'])
        totalsamples = int(i['info']['TotalSamples'])
        duration = float(i['info']['Duration'])
        finfo = (f"Input audio info:\n"
                 f"CompressionMethod: {compress}\n"
                 f"NumChannels: {channels}\n"
                 f"SampleRate: {samplerate} Hz\n"
                 f"TotalSamples: {totalsamples}\n"
                 f"Duration: {duration} s"
                 )
        yield {'t': 'text', 'v': finfo}
        #-------------------------------------------------------------------------

        if duration < 15.0:
            yield {'t': 'text', 'v': f"WARNING: The length of the audio file is {duration} seconds.\nMore than 15 seconds required."}
        #-------------------------------------------------------------------------
        waveform = self.waveform(fn)
        yield waveform
