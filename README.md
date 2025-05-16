<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![GNU-GPL-v3][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/nikolisan/xb-gui">
    <img src="images/xb-gui-logo-small.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">xb-gui</h3>

  <p align="center">
    a simple but effective way to create XBeach 2DV models
    <br />
    <a href=""><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/nikolisan/xb-gui/issues/new?labels=bug&template=bug_report.md">Report Bug</a>
    &middot;
    <a href="https://github.com/nikolisan/xb-gui/issues/new?labels=enhancement&template=feature_request.md">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

<!-- [![Product Name Screen Shot][product-screenshot]](https://example.com) -->

**xb-gui** is a simple yet effective tool for creating models for XBeach. Its primary focus is on developing models in a 2D-V configuration (cross-shore profiles), but it also includes additional features to support users with tasks such as:
* Extracting cross-shore profiles from DEMs
* Loading and editing on-the-fly storm sequences, water level conditions, input profile
* Creating batch run sets *[WIP]*
It was primarly created for creating models for the gravel variant of XBeach, XBeach-G.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

[![Python][python-shield]][Python-url] [![Miniforge][miniforge-shield]][miniforge-url]


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

The project is build using _miniforge_. Use `conda` or any other environment manager, such as `pipenv` to get a working installation.

*Clone the repo*
   ```sh
   git clone https://github.com/nikolisan/xb-gui.git
   ```
   > ℹ If you do not have a `git` client, simply unzip the [source code repository](https://github.com/nikolisan/xb-gui/archive/master.zip).

### Installation using `conda`

1. Create conda environment
   ```sh
   conda env create -f environment.yml
   ```
2. Activate conda environment
   ```sh
   conda activate myenv
   ```
3. Verify the environment is properly installed
   ```sh
   conda env list
   ```

### Installation using `pipenv`

1. Make sure you have `pipenv` installed
    ```sh
    pip --version
    pip install --user pipenv
    ```
2. Install packages
    ```sh
    cd xb-gui
    pipenv install --ignore-pipfile
    ```

### Installation using `pip`

If you'd like to use your own virtual environment manager, use pip to install the dependencies.
```sh
pip install -r requirements.txt
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

1. Change directory to the root folder, if not already
    ```sh
    cd xb-gui
    ```
2. Start the application
    * Run using `conda`
        ```sh
        conda activate xb-gui
        python main.py
        ```
    * Run using `pipenv`
        ```sh
        pipenv run python main.py
        ```
    * Run using plain python
        ```sh
        python main.py
        ```
3. Alternatively, you can download the standalone executable from the releases. At the moment, only _Windows x86_64_ is supported.


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [⏳] Prepare XBeach model
    - [⏳] Setup grid
    - [✅] Setup initial conditions and inputs
    - [⏳] Simulation parametes dictionary
    - [⏳] Export model folder
- [⏳] Run XBeach separately
- [⏳] Analyse xbeach results
- [⏳] Prepare multiple profiles
    - [⏳] Setup batch runs
- [⏳] Add functionality for Project structure
    - [⏳] Create a new project
    - [⏳] Load a project
- [⏳] Extra tools
    - [✅] Extract from raster

See the [open issues](https://github.com/nikolisan/xb-gui/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Top contributors:

<a href="https://github.com/nikolisan/xb-gui/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=nikolisan/xb-gui" alt="contrib.rocks image" />
</a>



<!-- LICENSE -->
## License

Distributed under the GNU-GPL-v3. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

<!-- Your Name - [@twitter_handle](https://twitter.com/twitter_handle) - email@email_client.com -->

Project Link: [https://github.com/nikolisan/xb-gui](https://github.com/nikolisan/xb-gui)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments
The UI is inspired by [PyTelTools-GUI](https://github.com/CNR-Engineering/PyTelTools) and the [DHI MIKE](https://www.dhigroup.com/technologies/mikepoweredbydhi) software suite.

Other:
* [Othneil Drew's Best-README-Template](https://github.com/othneildrew/Best-README-Template)
* [GitHub Emoji Cheat Sheet](https://www.webpagefx.com/tools/emoji-cheat-sheet)
* [Img Shields](https://shields.io)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/nikolisan/xb-gui.svg?style=for-the-badge
[contributors-url]: https://github.com/nikolisan/xb-gui/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/nikolisan/xb-gui.svg?style=for-the-badge
[forks-url]: https://github.com/nikolisan/xb-gui/network/members
[stars-shield]: https://img.shields.io/github/stars/nikolisan/xb-gui.svg?style=for-the-badge
[stars-url]: https://github.com/nikolisan/xb-gui/stargazers
[issues-shield]: https://img.shields.io/github/issues/nikolisan/xb-gui.svg?style=for-the-badge
[issues-url]: https://github.com/nikolisan/xb-gui/issues
[license-shield]: https://img.shields.io/github/license/nikolisan/xb-gui.svg?style=for-the-badge
[license-url]: https://github.com/nikolisan/xb-gui/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/xb-gui-logo-small.png

[python-shield]:https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoSize=auto&logoColor=fff
[Python-url]:https://www.python.org/
[miniforge-shield]:https://img.shields.io/badge/miniforge-000?style=for-the-badge&logo=conda-forge&logoSize=auto&labelColor=000
[miniforge-url]:https://github.com/conda-forge/miniforge
