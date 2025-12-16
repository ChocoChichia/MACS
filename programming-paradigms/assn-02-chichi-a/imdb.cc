using namespace std;
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <unistd.h>
#include "imdb.h"
#include <stdio.h>
#include <string.h>

const char *const imdb::kActorFileName = "actordata";
const char *const imdb::kMovieFileName = "moviedata";

struct actorData
{
  const void *actorFile;
  const string *name;
};

struct movieData
{
  const void *movieFile;
  film movie;
};

imdb::imdb(const string &directory)
{
  const string actorFileName = directory + "/" + kActorFileName;
  const string movieFileName = directory + "/" + kMovieFileName;

  actorFile = acquireFileMap(actorFileName, actorInfo);
  movieFile = acquireFileMap(movieFileName, movieInfo);
}

bool imdb::good() const
{
  return !((actorInfo.fd == -1) ||
           (movieInfo.fd == -1));
}

bool imdb::getCredits(const string &player, vector<film> &films) const
{

  //create a struct from given actor
  actorData actor;
  actor.actorFile = actorFile;
  actor.name = &player;

  //number of actors in our file
  int actor_count = *((int *)actorFile);

  //bsearch to find our actors location in actorfile
  int *loc = (int *)bsearch(&actor, (int *)actorFile + 1, actor_count, sizeof(int), compareActors);

  if (loc == NULL)
    return false;
  int location = *loc;

  int len = player.size() + 1;
  // Making sure our short will be on eventh memory block
  if (len % 2 != 0)
  {
    len++;
  }

  // number of moveis actor has participated in
  short movie_num = *(short *)((char *)actorFile + location + len);
  len += 2;

  if (len % 4 != 0)
    len += 2;

  // Starting location for movies our actor participated in 
  const void *movies_loc = (char *)actorFile + location + len;

  for (int i = 0; i < movie_num; i++)
  { 
    // we retrieve byte location of movie number i 
    int offset_i = *(int *)((char *)movies_loc + i * sizeof(int));
    // using location above we get name and year for movie number i
    string m_name = (char *)movieFile + offset_i;
    int year = 1900 + *(char *)(movieFile + offset_i + m_name.size() + 1);

    //now we creat a film using retrieved name and year and push in our vector
    film f;
    f.title = m_name;
    f.year = year;
    films.push_back(f);
  }

  return true;
}

bool imdb::getCast(const film &movie, vector<string> &players) const
{

  // Creating sttruct using our movie
  movieData film;
  film.movieFile = movieFile;
  film.movie = movie;

  //number of moveis in moviefile
  int movies_count = *(int *)(movieFile);

  //retrieving location of our movie in moveifile with bsearch 
  int location = *(int *)bsearch(&film, (int *)movieFile + 1, movies_count, sizeof(int), compareMovies);

  if (location == NULL)
    return false;

  int len = movie.title.size() + 1 + 1; //additioanl 1 is added to omit year char

  // to make sure short is stored in eventh block
  if (len % 2 != 0)
    len++;
  
  // ptr is pointing to specific movies datas begginning
  const void *ptr = (char *)movieFile + location;

  // we retrieve number of actor who played in this movie
  short actor_num = *(short *)((char *)ptr + len);

  len += 2;

  if (len % 4 != 0)
    len += 2;

  for (int i = 0; i < actor_num; i++)
  {
    // we get the byte location of actor number i ( in actorfile )
    int i_offset = *(int *)((char *)ptr + len + i * sizeof(int));
    // from actorfile we retrieve actors name
    string name = (const char *)actorFile + i_offset;
    players.push_back(name);
  }

  return true;
}

imdb::~imdb()
{
  releaseFileMap(actorInfo);
  releaseFileMap(movieInfo);
}

// ignore everything below... it's all UNIXy stuff in place to make a file look like
// an array of bytes in RAM..
const void *imdb::acquireFileMap(const string &fileName, struct fileInfo &info)
{
  struct stat stats;
  stat(fileName.c_str(), &stats);
  info.fileSize = stats.st_size;
  info.fd = open(fileName.c_str(), O_RDONLY);
  return info.fileMap = mmap(0, info.fileSize, PROT_READ, MAP_SHARED, info.fd, 0);
}

void imdb::releaseFileMap(struct fileInfo &info)
{
  if (info.fileMap != NULL)
    munmap((char *)info.fileMap, info.fileSize);
  if (info.fd != -1)
    close(info.fd);
}

// function receives actor as a key and compares the key
// to another actor located in "offset"th byte in actorfile
int compareActors(const void *actor, const void *offset)
{
  // copy our actors pointer as actordata type struct 
  actorData *ad = (actorData *)actor;
  // byte location of a pointer we'll compare to our ad/actor
  int byte_num = *(int *)offset;

  const char *name2 = (const char *)ad->actorFile + byte_num; 
  const char *name1 = ad->name->c_str();

  return strcmp(name1, name2); 
}
//function receives movie as a key and compares the key ro another
// movie located in specified offset in movie file
int compareMovies(const void *mov, const void *offset)
{

  movieData *md = (movieData *)mov;
  int location = *(int *)offset; 

  film film1 = md->movie;
  film film2;

  const void *ptr = md->movieFile + location;
  film2.title = (char *)ptr; 
  film2.year = 1900 + *((char *)ptr + film2.title.size() + 1);

  int compare = strcmp(film1.title.c_str(), film2.title.c_str());
  
  //if names are the same we compare by years 
  if (compare == 0)
  {
    return film1.year - film2.year;
  }
  else
  {
    return compare;
  }
}
