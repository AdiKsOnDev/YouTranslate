import unittest 
import sys
import os

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(path)
sys.path.insert(0, path)

from unittest.mock import patch, mock_open
from modules.helperFunctions import get_transcript_no_delay, get_transcript, installVideo, extract_audio, replace_audio, get_translation

class TestHelperFunctions(unittest.TestCase):

    @patch('modules.helperFunctions.YouTubeTranscriptApi.get_transcript')
    def test_get_transcript_no_delay(self, mock_get_transcript):
        mock_get_transcript.return_value = [{'text': 'test'}]
        with patch("builtins.open", mock_open()) as mock_file:
            get_transcript_no_delay('3JNEDnl8XXA', 'no_delay.txt')
            mock_file().write.assert_called_with('\n')

    @patch('modules.helperFunctions.get_transcript')
    def test_get_transcript(self, mock_get_transcript):
        mock_get_transcript.return_value = [{'text': 'test', 'start': 0, 'duration': 0}]
        with patch("builtins.open", mock_open()) as mock_file:
            get_transcript('3JNEDnl8XXA', 'no_delay.txt')
            mock_file().write.assert_called_with('\n')

    @patch('modules.helperFunctions.YouTube')
    def test_installVideo(self, mock_youtube):
        mock_youtube.return_value.streams.filter().first().download.return_value = None
        self.assertEqual(installVideo('https://www.youtube.com/watch?v=3JNEDnl8XXA'), 0)
        
if __name__ == '__main__':
    unittest.main()