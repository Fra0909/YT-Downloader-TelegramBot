from pytube import YouTube
import datetime
import os


class YtDownloader():

    def __init__(self, link, path):
        self.link = link
        self.path = path
        self.downloader = YouTube(self.link)

    def get_video_info(self):
        info = {}
        info['author'] = self.downloader.author
        info['length'] = str(datetime.timedelta(seconds=self.downloader.length))[2:]
        info['title'] = self.downloader.title
        info['publish_date'] = datetime.datetime.strftime(self.downloader.publish_date, '%d-%m-%Y')
        info['views'] = self.downloader.views
        return info


    def download_video(self):
        # self.downloader.streams.filter().first().download(self.path)
        streams = self.downloader.streams.order_by('resolution').filter(progressive=True)
        smallest = streams.last()
        for i in range(len(streams)):
            if streams[i].filesize < smallest.filesize:
                smallest = streams[i]
        if smallest.filesize < 52427799:
            smallest.download(self.path)
            return True
        return False
#Trying to find the stream with the highest resolution and a file size lower than 50MB.


    def get_video_path(self):
        return self.path + '/' + os.listdir(self.path)[0]

    def delete_video(self):
        os.remove(self.path + '/' + os.listdir(self.path)[0])

def main(url):
    yt = YtDownloader(url,'videos')
    if yt.download_video():
        return yt.get_video_path(), yt.get_video_info()
    return None

if __name__ == '__main__':
    main()



