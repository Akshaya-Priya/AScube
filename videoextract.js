const { google } = require('googleapis');

// Replace with your own API key
const API_KEY = 'YOUR_YOUTUBE_API_KEY';

// Initialize the YouTube Data API
const youtube = google.youtube({
  version: 'v3',
  auth: API_KEY,
});

async function fetchPlaylistVideos(playlistId) {
  try {
    let nextPageToken = null;
    let videos = [];

    do {
      const response = await youtube.playlistItems.list({
        part: 'snippet',
        playlistId: playlistId,
        maxResults: 50, // Maximum results per page (can be adjusted)
        pageToken: nextPageToken,
      });

      nextPageToken = response.data.nextPageToken;
      const playlistItems = response.data.items;

      playlistItems.forEach(item => {
        const videoId = item.snippet.resourceId.videoId;
        const videoTitle = item.snippet.title;
        videos.push({ videoId, videoTitle });
      });
    } while (nextPageToken);

    return videos;
  } catch (error) {
    console.error('Error fetching playlist videos:', error.message);
    throw error;
  }
}

// Example usage:
const playlistId = 'YOUR_PLAYLIST_ID'; // Replace with the ID of the YouTube playlist
fetchPlaylistVideos(playlistId)
  .then(videos => {
    console.log('Videos in the playlist:');
    videos.forEach(video => {
      console.log(`${video.videoTitle} - https://www.youtube.com/watch?v=${video.videoId}`);
    });
  })
  .catch(err => {
    console.error('Error:', err);
  });
