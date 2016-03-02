from moviepy.editor import VideoFileClip, concatenate_videoclips

clip1 = VideoFileClip("partly_cloudy.mp4").subclip(747, 759)
clip1.fps = 15
clip1.write_videofile("partly_cloudy_short.mp4")