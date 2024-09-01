---
# Python Requirements
The reciperave project requires python version 3.10.4

# RecipeRave

RecipeRave is an innovative online platform crafted specifically for passionate culinary enthusiasts seeking a vibrant community to engage with and explore their love for cooking and baking. With its intuitive and user-friendly interface, RecipeRave provides a welcoming space for individuals to discover, share, and celebrate their favorite recipes from around the globe. Users are not only invited to access an extensive collection of diverse recipes but also to actively participate in the thriving community by contributing their own culinary creations and engaging with others through comments, ratings, and discussions. Whether it's a traditional family recipe passed down through generations or a modern twist on a classic dish, RecipeRave encourages users to share their culinary expertise and creativity with like-minded individuals, fostering a collaborative and inspiring environment for culinary exploration and discovery.


## Modules & Description

- **Recipe Collections**: Allow users to create and curate their own collections of recipes based on themes, occasions, or personal preferences. This feature enhances organization and makes it easier for users to access and share groups of recipes they love.

- **Cooking Videos**: Integrate cooking tutorial videos alongside recipes to provide visual guidance for users. These videos can be uploaded by users or sourced from external platforms, offering an interactive and multimedia-rich experience for learning new recipes.

- **User Authentication**: This module ensures that users can securely register, log in, and manage their accounts. It establishes a personalized experience for each user, allowing them to contribute to the community by sharing recipes and engaging with others.

- **Recipe Management**: This module enables users to upload, edit, and manage their recipes. It forms the core functionality of the website, facilitating the sharing of culinary creations among the community members.

- **Search and Filtering**: With this module, users can easily discover recipes based on specific criteria such as cuisine, meal type, ingredients, or difficulty level. It enhances user experience by providing efficient navigation through the extensive recipe collection.

- **Rating and Comments**: This module encourages user engagement by allowing them to rate and comment on recipes shared by others. It facilitates interaction within the community, enabling users to share feedback, tips, and experiences related to each recipe.

- **Social Sharing**: Integrating social media sharing options would allow users to easily share their favorite recipes or interactions on RecipeRave with their friends and followers on various social platforms.

- **Bookmarking**: Providing a feature for users to bookmark or save recipes they're interested in for future reference can improve user engagement and retention.

- **User Profiles**: Enhancing user profiles with features like bio sections, profile pictures, and activity feeds can foster a sense of community and enable users to connect with each other more easily.

- **Follow User**: Implementing a "Follow User" feature would allow users to stay updated on the activities and recipe uploads of their favorite cooks and culinary influencers. This feature fosters a sense of community and enables users to discover new recipes and culinary inspiration from those they admire.

- **Feedback System**: Introducing a feedback system where users can provide suggestions, report issues, or offer general feedback about the website's functionality and content. This system can help the platform improve over time by addressing user concerns and continuously enhancing the user experience.

- **Admin Panel**: A backend module that allows administrators to manage user accounts, review and moderate recipe submissions, monitor site activity, and perform other administrative tasks to ensure the smooth operation and integrity of the RecipeRave platform.

## Installation

To install the RecipeRave project, simply clone the repository and install the required dependencies:

```
git clone https://github.com/Bineesh627/reciperave.git
cd reciperave/reciperave
pip install -r requirements.txt
```

## Usage

```
python manage.py runserver
```

## Initialization commands

To create a Django project, use the following command:

```
django-admin startproject <project name>
```

To create an app in Django, use the following command:

```
django-admin startapp <app name>
```

To create a superuser in Django for the admin login page, use the following command:

```
python manage.py createsuperuser
```

Run the collectstatic command to gather all static files into the STATIC_ROOT directory after ensuring the directory exists and settings are correct.

```
python manage.py collectstatic
```

To create new migrations based on model changes.

```
python manage.py makemigrations
```

To apply these migrations to the database.

```
python manage.py migrate
```

## Contribution

Contributions are welcome! If you encounter any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

---
