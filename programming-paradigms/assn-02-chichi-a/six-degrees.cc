#include <vector>
#include <list>
#include <set>
#include <string>
#include <iostream>
#include <iomanip>
#include "imdb.h"
#include "path.h"
using namespace std;

/**
 * Using the specified prompt, requests that the user supply
 * the name of an actor or actress.  The code returns
 * once the user has supplied a name for which some record within
 * the referenced imdb existsif (or if the user just hits return,
 * which is a signal that the empty string should just be returned.)
 *
 * @param prompt the text that should be used for the meaningful
 *               part of the user prompt.
 * @param db a reference to the imdb which can be used to confirm
 *           that a user's response is a legitimate one.
 * @return the name of the user-supplied actor or actress, or the
 *         empty string.
 */

static string promptForActor(const string& prompt, const imdb& db)
{
  string response;
  while (true) {
    cout << prompt << " [or <enter> to quit]: ";
    getline(cin, response);
    if (response == "") return "";
    vector<film> credits;
    if (db.getCredits(response, credits)) return response;
    cout << "We couldn't find \"" << response << "\" in the movie database. "
	 << "Please try again." << endl;
  }
}


//method for generating path
bool generateShortestPath(string& source,  string& target, imdb& db, path &foundPath){
  
  list<path> partialPaths;  // here we store every path on our way
  set<string> previouslySeenActors; 
  set<film> previouslySeenFilms;

  partialPaths.push_back(path(source));

  while (!partialPaths.empty() && partialPaths.front().getLength() <= 5) {
    
    path p = partialPaths.front();
    partialPaths.pop_front(); 

    // starting from the last actor in our path we add
    // actors connected to the latest
    string act_name = p.getLastPlayer();
    vector<film> movies;

    // retrieving moveis our latest actor has stared in
    db.getCredits(act_name, movies);
    
    for (const auto& f : movies) {
      if (previouslySeenFilms.find(f) != previouslySeenFilms.end()) 
        continue;
      previouslySeenFilms.insert(f);

      //for each movie now we generate its cast to 
      //generate every actor connected to our latest actor from path
      vector<string> actors;
      db.getCast(f, actors);

      for (const string& a : actors) {
        if (previouslySeenActors.find(a) != previouslySeenActors.end()) 
          continue;

        path next_path = p;
        next_path.addConnection(f, a);

        //if we found the target form this movies cast we end our loop
        if (a == target) {
          foundPath = next_path;
          return true;
        }

        // we continue to add "connected to each other" actors in the path until we find the target
        partialPaths.push_back(next_path);
        previouslySeenActors.insert(a);  
      }
    }
  }

  return false;
}

/**
 * Serves as the main entry point for the six-degrees executable.
 * There are no parameters to speak of.
 *
 * @param argc the number of tokens passed to the command line to
 *             invoke this executable.  It's completely ignored
 *             here, because we don't expect any arguments.
 * @param argv the C strings making up the full command line.
 *             We expect argv[0] to be logically equivalent to
 *             "six-degrees" (or whatever absolute path was used to
 *             invoke the program), but otherwise these are ignored
 *             as well.
 * @return 0 if the program ends normally, and undefined otherwise.
 */

int main(int argc, const char *argv[])
{
  imdb db(determinePathToData(argv[1]));
  if (!db.good()) {
    cout << "Failed to properly initialize the imdb database." << endl;
    cout << "Please check to make sure the source files exist and that you have permission to read them." << endl;
    return 1;
  }
  
  while (true) {
    string source = promptForActor("Actor or actress", db);
    if (source == "") break;
    string target = promptForActor("Another actor or actress", db);
    if (target == "") break;
    if (source == target) {
      cout << "Good one.  This is only interesting if you specify two different people." << endl;
    } else {
      path found_path(source);
      bool result = generateShortestPath(source, target, db, found_path);
      if (result) {
        cout << endl << found_path << endl;
      }
      else {
        cout << endl << "No path between those two people could be found." << endl << endl;
      }
    }
  }
  
  cout << "Thanks for playing!" << endl;
  return 0;
}

