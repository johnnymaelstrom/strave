import argparse
import sys
import wave
import struct

def main():
    parser = argparse.ArgumentParser(description='Process a GPX file.')
    parser.add_argument('filename', type=str, help='The GPX file to process')
    
    args = parser.parse_args()
    
    print(f'Processing file: {args.filename}')

    import xml.etree.ElementTree as ET

    def parse_gpx(filename):
        tree = ET.parse(filename)
        root = tree.getroot()
        
        ns = {'default': 'http://www.topografix.com/GPX/1/1'}
        
        data = []
        
        for trkpt in root.findall('.//default:trkpt', ns):
            ele = trkpt.find('default:ele', ns)
            time = trkpt.find('default:time', ns)
            
            if ele is not None and time is not None:
                data.append((time.text, float(ele.text)))
        
        return data

    data = parse_gpx(args.filename)

    for time, ele in data:
        print(f'{time}, {ele}')

        print(f'Number of elevation points: {len(data)}')

    #def write_wav(filename, data, sample_rate=44100):
    #wavetable format is: 1 channel, 16 bits containing 256 2-byte samples per waveform with 64 waveforms in total
    
    def write_wav(filename, data, sample_rate=16000):
        with wave.open(filename, 'w') as wav_file:
            n_channels = 1
            sampwidth = 2
            n_frames = len(data)
            comptype = 'NONE'
            compname = 'not compressed'
            
            wav_file.setparams((n_channels, sampwidth, sample_rate, n_frames, comptype, compname))
            
            for sample in data[:256]:
                wav_file.writeframes(struct.pack('h', int(sample)))

    elevation_data = [ele for _, ele in data]
    output_wav_file = args.filename.replace('.gpx', '.wav')
    write_wav(output_wav_file, elevation_data)
    
    print(f'WAV file created: {output_wav_file}')

    

if __name__ == '__main__':
    main()