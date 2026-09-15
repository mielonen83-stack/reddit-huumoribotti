import { Devvit } from '@devvit/public-api';
import { reddit } from '@devvit/reddit';

Devvit.configure({
  redditAPI: true,
});

// Funktio, joka hakee videot r/funny -kanavalta
export async function haeHuumorivideot() {
  try {
    const listings = await reddit.getHotPosts({
      subredditName: 'funny',
      limit: 25,
    });

    const videot = [];

    for await (const post of listings) {
      if (post.isVideo || post.url?.includes('v.redd.it')) {
        videot.push({
          title: post.title,
          score: post.score,
          url: post.url,
          permalink: `https://reddit.com${post.permalink}`,
        });
      }
    }

    return videot;
  } catch (error) {
    console.error('Virhe haussa:', error);
    return [];
  }
}
