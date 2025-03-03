

def create_movie(movie_title, genre, rating):
    """ 
        Creates a movie dictionary with the following structure
        {"title": movie_title,
            "genre": genre,
            "rating": rating}
        If any of the information is missing, it returns None
        INPUT: string, string, float
        OUTPUT: a movie dictionary or None
    """
    if not movie_title or not genre or not rating:
        return None

    return {"title": movie_title,
            "genre": genre,
            "rating": rating
            }


def add_to_watched(user_data, movie):
    """
        Adds a movie to the user's watched list
        INPUT: user_data dictionary, movie dictionary
        OUTPUT: updated user_data dictionary
    """
    user_data["watched"].append(movie)
    return user_data


def add_to_watchlist(user_data, movie):
    """
        Adds a movie to the user's watchlist
        INPUT: user_data dictionary, movie dictionary
        OUTPUT: updated user_data dictionary
    """
    user_data["watchlist"].append(movie)
    return user_data


def watch_movie(user_data, movie_title):
    """
        Finds a movie dictionary that corresponds to movie_title
        in the user's watchlist (if any), removes it from watchlist 
        and adds it to the watched list
        If the movie_title wasn't on the watchlist it returns the 
        unchanged user_data
        INPUT: user_data dictionary, movie title string
        OUTPUT: updated user_data dictionary
    """
    for movie in user_data["watchlist"]:
        if movie["title"] == movie_title:
            watched_movie = movie
            user_data["watchlist"].remove(watched_movie)
            user_data = add_to_watched(user_data, watched_movie)
            return user_data
    return user_data


def get_watched_avg_rating(user_data):
    """
        Calculates the average rating from the movies
        the user has watched
        If user_data["watched"] is empty, it returns 0
        INPUT: user_data dictionary
        OUTPUT: float
    """
    if not user_data["watched"]:
        return 0.0
    ratings = [movie["rating"] for movie in user_data["watched"]]
    return sum(ratings) / len(ratings)


def get_most_watched_genre(user_data):
    """
        Finds the most frequently watched genre the user has watched,
        in case of a tie it only returns one genre
        If user_data["watched"] is empty, it returns None
        INPUT: user_data dictionary
        OUTPUT: genre string or None
    """
    if not user_data["watched"]:
        return None
    genres = [movie["genre"] for movie in user_data["watched"]]
    return get_most_frequent(genres)


def get_unique_watched(user_data):
    """
        Returns a list of all movies that the user watched 
        that none of their friends has watched
        INPUT: user_data dictionary
        OUTPUT: list of movie dictionaries
    """
    friend_watched_titles = set(
        [movie["title"] for friend in user_data["friends"]
         for movie in friend["watched"]])

    return [movie for movie in user_data["watched"]
            if movie["title"] not in friend_watched_titles]


def get_friends_unique_watched(user_data):
    """
        Returns a list of all movies that the user has not watched,
        but at least one of their friends has, without repetitions.
        INPUT: user_data dictionary
        OUTPUT: list of movie dictionaries
    """
    friends_watched_movies = (
        movie for friend in user_data["friends"] for movie in friend["watched"])

    friends_watched_movies_dict = {
        movie["title"]: movie for movie in friends_watched_movies}

    user_watched_titles = set([movie["title"]
                               for movie in user_data["watched"]])

    friends_unique_watched_movies = [
        movie for title, movie in friends_watched_movies_dict.items()
        if title not in user_watched_titles]

    return friends_unique_watched_movies


def get_available_recs(user_data):
    """
        Returns a list of all unique movies that the user has not watched,
        but at least one of their friends has, that are hosted in 
        a subscription service the user has access to
        INPUT: user_data dictionary
        OUTPUT: list of movie dictionaries
    """
    possible_recs = get_friends_unique_watched(user_data)
    return [movie for movie in possible_recs
            if movie["host"] in user_data["subscriptions"]]


def get_new_rec_by_genre(user_data):
    """
        Returns a list of all unique movies of the user's preferred genre
        that the user has not watched and at least one of their friends has
        If user_data["watched"] is empty, it returns an empty list
        INPUT: user_data dictionary
        OUTPUT: list of movie dictionaries
    """
    if not user_data["watched"]:
        return []
    preferred_genre = get_most_watched_genre(user_data)
    possible_recs = get_friends_unique_watched(user_data)
    return [movie for movie in possible_recs
            if movie["genre"] == preferred_genre]


def get_rec_from_favorites(user_data):
    """
        Returns a list of all unique movies from the user's favorite movies
        that their friends have not watched
        INPUT: user_data dictionary
        OUTPUT: list of movie dictionaries
    """
    possible_rec_titles = [movie["title"]
                           for movie in get_unique_watched(user_data)]

    return [movie for movie in user_data["favorites"]
            if movie["title"] in possible_rec_titles]


def get_most_frequent(genres):
    """
        Returns the most frequent element of a list 
        or one of the most frequent in case of a tie
        INPUT: list
        OUTPUT: most frequent element of the list
    """
    count = {}
    for genre in genres:
        count[genre] = count.get(genre, 0) + 1
    return max(count, key=lambda x: count[x])
