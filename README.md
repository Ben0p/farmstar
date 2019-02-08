# Farmstar
Farm management system.

## Changes in version 2
*Abandoning version 1*

- Complete re-write after much learnings
- Dropping windows support
    - Dual OS support too time consuming
    - Might reinstate in the future
- Using mongoDB rather than sqlite
    - NoSQL easier for json objects and restAPI
    - Allows for separate server if required
- Using Flask restful API
    - No reason apart from familiarity
- Utilizing https://github.com/akveo/ngx-admin UI
    - Awesome looking angular dashboard
- Stucturing scripts as linux services
    - Easier start / stop on boot
- Dropping curses backend display
    - All information will be available through frontend WebUI


## License
[GNU GPL](LICENSE)