# Views
:octocat:
Welcome to the views folder! In here, we have functions serving the endpoints directly. Much of the parsing for required argument goes here.
This server's clients can be divided into two crowds: apps and iot devices.

Let's go over the endpoints regarding Niche first
### For Niche
* `/device/register` allowed methods [POST]
    * POST 
        Registers the niche device, creating a logical representation in the database so its stamps can be recorded. Requires auth.

* `/device` allowed methods [POST]
    * POST
        Records a reading from a niche. 

### For App

* `/dashboard` allowed methods [GET]    **NOT YET IMPLEMENTED**
    * POST
        Gets the relevant information for user's niche devices. Requires auth.

* `/family/register` allowed methods [POST]
    * POST
        Registers a family, which is the logical representation of the owner of the Niches. There can be multiple members inside a family with varying authorities. Requires auth.

* `/member/register` allowed methods [POST]
    * POST
        Registers a member, which needs to be inside a family.

* `/signin` allowed methods [POST]
    * POST
        Signs the user in, generating a token

* `/checkout` allowed methods [POST]
    * POST
        Equivalent stub for the checkout. Currently stores the items bought and alerts our delivery people by email.

* `/listtocart` allowed methods [DELETE, POST, PUT]
    * DELETE
        Deletes the specified list_to_cart record
    * POST
        Switches the list_to_cart record between shopping list and shopping cart
    * PUT 
        Updates or changes the specified list_to_cart record

*  `/listtocart/list` allowed methods [GET, POST]
    * GET
        Gets all the items in the family's list
    * POST 
        Registers new list_to_cart item

*   `/listtocart/cart` allowed methods [GET]
    * GET
        Gets all the items in the family's shopping cart
