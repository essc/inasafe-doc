.. image:: /static/training/intermediate/qgis-inasafe/image6.*

Module 5: Calculating Damages and Losses
========================================

**Learning Objectives**

- Explain the definition of damages, losses, and their calculation based on
  exposure data from OSM/community participation which is impacted by disasters
- Explain damage and losses assessment values based on BNPB and BPBD
- Making damage and losses map
- Calculate damage area
- Manipulate attributes data of affected features to obtain damage values for
  each object
- Manipulate attributes data of affected features to obtain losses values for
  each object
- Grouping attributes data for each administration area (hamlet, village,
  subdistrict)
- Join attribute data for each administration area (hamlet, village,
  subdistrict)
- Present damages and losses value using charts

**A Damage and Loss Assessment (DaLA)** is usually created after after a
disaster.
The standard DaLA methodology was developed by the UN Economic Commission for
Latin America and the Caribbean (UN-ECLAC) in 1972,
and has evolved with various international organizations since.
Simply, it is a methodology for approximating damage and losses due to a
disaster, basing calculations on a country’s economy and individual
livelihoods to define the needs for recovery and reconstruction.

A Damage and Loss Assessment includes the following:

- Damage calculated as the replacement value of totally or partially destroyed
  physical assets;
- Losses in the flows of  economy that arise from the temporary absence of the
  damaged assets;
- The resultant impact on post-disaster macroeconomic performance, with special
  reference to economic growth/GDP, the balance of payments and fiscal situation
  of the Government.

In this Module we will learn how to calculate some of the basic data used in a
DaLA, and use various QGIS functions to design a thematic map that shows
damage and loss.

**1. BPBD Damage Assessment Guide**

The BPBD has created a guide for damage and loss assessment for Indonesia,
which defines varying degrees of damage and the economic impact of individual
elements.
Parts of this definition are shown here:

These are the guidelines for **Damage & Loss Assessment.**

.. image:: /static/training/intermediate/qgis-inasafe/image82.*
   :align: center

Notice that there are several elements at work here.  First,
damage to different types of infrastructure is “valued” differently.
To put losses into monetary terms, a the loss of a bridge has a loss value as
does the loss of a public building or a private home.
Then, depending on whether a feature suffers heavy, medium, or low damage,
a multiplier is applied to determine the value of the loss.

By adding up all of the damage it is possible to assess the total damages
caused by a disaster.
In the remainder of this Module, we will calculate the value of the losses in
our Sirahan project, and see how we can display them graphically using our
map, based on the damage suffered in each hamlet.

**2. Damage and Losses Assessment Map**

We will create a Damage and Loss Assessment Map using our data from Sirahan
Village that we have been working with throughout this module.

- Open QGIS and make sure that the following layers are loaded into your project:
    - area_terdampak_Sirahan
    - Jalan_Sirahan
    - Sungai_Sirahan
    - Batas_Desa_Sirahan
    - Bangunan_Sirahan

.. image:: /static/training/intermediate/qgis-inasafe/image83.*
   :align: center

We will assume that all the buildings in the area_terdampak_Sirahan layer
(hazard zone) suffered heavy damage from the disaster.
Let’s create a spatial query to filter out these buildings.

- Go to :menuselection:`Vector > Spatial Query > Spatial Query` and enter the
  fields like this:

.. image:: /static/training/intermediate/qgis-inasafe/image84.*
   :align: center

- We now have a bunch of buildings selected which we are assuming will suffer
  heavy damages.
  According to the BNPB Guide, we can assess the loss of heavily damaged
  buildings at a rate of 1.8million Rp. / square meter,
  and the multiplier factor is 70%.
  Our formula for calculating losses is:

*Total Building area x Loss Value per m² x Multiplier factor*

- Therefore we want to calculate:

**Total Building Area x 1.8 million Rp. x 70%**

in order to get a calculation of the value of total losses.

- We will use the Intersect Geoprocessing tool so that we can combine
  attributes from our district layer with the selection of buildings we have
  just made.
  Go to :menuselection:`Vector > Geoprocessing Tools > Intersect` and fill in
  the fields as follows:

.. image:: /static/training/intermediate/qgis-inasafe/image85.*
   :align: center

- Save the result as Bangunan_Terdampak_perDusun.
- Hide the original buildings layer so that your map looks like this:

.. image:: /static/training/intermediate/qgis-inasafe/image86.*
   :align: center

- Since we used the intersect tool. Our attribute table will include the DUSUN
  attribute.

.. image:: /static/training/intermediate/qgis-inasafe/image87.*
   :align: center

**3. Calculate Damage Area**

- On the attribute table of Bangunan_Terdampak_perDusun, click the
  :guilabel:`Toggle Editing` button.

.. image:: /static/training/intermediate/qgis-inasafe/image88.*
   :align: center

- Then click the :guilabel:`New Column` button.

.. image:: /static/training/intermediate/qgis-inasafe/image89.*
   :align: center

- Create a new column named “Damage” of type decimal number:

.. image:: /static/training/intermediate/qgis-inasafe/image90.*
   :align: center

- To calculate the damaged area of affected buildings we will use the field
  calculator to determine the number of square meters in each building feature.
  Click on :guilabel:`Field Calculator`.

.. image:: /static/training/intermediate/qgis-inasafe/image91.*
   :align: center

- Check the box next to :guilabel:`Update existing field` and select
  “Damage_Area” in the dropdown box.
- Find :menuselection:`$area` under :guilabel:`Geometry` in the function list
  and double-click on it, so that it appears in the Expression box at the
  bottom.
  It should look like this:

.. image:: /static/training/intermediate/qgis-inasafe/image92.*
   :align: center

- Click :guilabel:`OK`.
  You will see that the column is filled in with the area, in square meters,
  of the buildings.

.. image:: /static/training/intermediate/qgis-inasafe/image93.*
   :align: center

- Click the :guilabel:`Toggle Editing` button and be sure to save your edits.

**4. Calculate Damages Using “Group Stats” Plugin**

We will be using a QGIS plugin called Group Stats in order to calculate damages
by each hamlet within Sirahan.
You will need to be connected to the internet to install this plugin.

- Go to :menuselection:`Plugins > Fetch Python Plugins`.
- Type “group stats” and when you find the plugin, select it and click
  :guilabel:`Install`.
- Once it is installed, go to
  :menuselection:`Plugins > Group Stats > Group Stats`

.. image:: /static/training/intermediate/qgis-inasafe/image94.*

- In :guilabel:`Choose vector layer` choose Bangunan_Terdampak_perDusun
- In :guilabel:`Choose classification field` fill in ‘DUSUN’
- In :guilabel:`Choose field attributes` fill in ‘Damage’.
- Click on :guilabel:`Calculate`  The results should look like this:

.. image:: /static/training/intermediate/qgis-inasafe/image95.*
   :align: center

- Select all the rows by clicking on the top row, holding :kbd:`SHIFT`, and
  clicking on the last row.
- Click :guilabel:`Save` and save it as BNG_Damages.

**5. Calculate Losses**

Now we’ve calculated the damaged area and we’ve created a table with damage
data for various hamlets in Sirahan.
Now let’s implement our losses formula in the wame way.

- Go back to the attribute table for Bangunan_Terdampak_perDusun and add a new
  column named “Losses.”

.. image:: /static/training/intermediate/qgis-inasafe/image96.*
   :align: center

- Once again, open the :guilabel:`Field Calculator`.
- Check :guilabel:`Update existing field` and choose “Losses”
- At the bottom in the Expression box, enter the following formula:

*“Damage” * 1800000 * 0.7*

.. image:: /static/training/intermediate/qgis-inasafe/image97.*
   :align: center

- Your new column is now filled with information calculated from this formula,
  which assesses the value of losses in Rp for each individual building.
  Save the layer and end the editing session.

**6. Calculating Losses Using “Group Stats” Plugin**

Now let’s calculate losses per hamlet using Group Stats again.

- In  :guilabel:`Choose vector layer` choose Bangunan_Terdampak_perDusun
- In :guilabel:`Choose classification field` type in ‘DUSUN’
- In :guilabel:`Choose field attributes` fill in ‘Losses’.
- Click :guilabel:`Calculate`.

.. image:: /static/training/intermediate/qgis-inasafe/image98.*
   :align: center

- The new table shows the losses in each hamlet.
- Select all the rows in the table and click :guilabel:`Save`. Save as
  BNG_Losses.

**7. Join Data**

Now we will join the tables that we created to our Batas_Desa_Sirahan attribute
table and then use them to add new columns to the file.

- Add the files BNG_Damages and BNG_Losses into QGIS, using
  :guilabel:`Add vector layer`

.. image:: /static/training/intermediate/qgis-inasafe/image99.*
   :align: center

- They will appear in your Layers list but not on your map,
  because they are not geographic data files, but rather tables.

.. image:: /static/training/intermediate/qgis-inasafe/image100.*
   :align: center

- Now we will perform an operation to join the layer Batas_Desa_Sirahan with
  BNG_Damage.
  Right click on the Batas_Desa_Sirahan layer and go to Properties.
- Go to the Joins tab:

.. image:: /static/training/intermediate/qgis-inasafe/image101.*
   :align: center

- Click the plus sign and fill in the following fields:
    - Join layer : BNG_Damages
    - Join field: DUSUN
    - Target field : DUSUN
- Click :guilabel:`OK`.
- Open the Attribute Table for Batas_Desa_Sirahan.
  You can see that the table we calculated with group stats is now attached
  to our attributes for each hamlet.
- Click :guilabel:`toggle editing` and choose :guilabel:`Field Calculator`.
- This time we will create a new field inside the field calculator.
  Fill in the top of the window like this:

.. image:: /static/training/intermediate/qgis-inasafe/image102.*
   :align: center

- Then in the expression box, enter *“Sum”*

.. image:: /static/training/intermediate/qgis-inasafe/image103.*
   :align: center

- Click :guilabel:`OK`.
  The BNG_Dmg column now contains the same value as column Sum in BNG_Damage
  .csv.
- As the damage values for each hamlet have been obtained we can delete the
  join.
  Right-click Batas_Desa_Sirahan, select properties, go to the
  :guilabel:`Join tab`, and click the minus button.

.. image:: /static/training/intermediate/qgis-inasafe/image104.*
   :align: center

- Now click the plus button, but this time join BNG_Losses in the same way as
  before:

.. image:: /static/training/intermediate/qgis-inasafe/image105.*
   :align: center

.. image:: /static/training/intermediate/qgis-inasafe/image106.*
   :align: center

- Open the attribute table for Batas_Desa_Sirahan, click toggle editing and open
  the :guilabel:`Field Calculator`.
  Fill in as follows:

.. image:: /static/training/intermediate/qgis-inasafe/image107.*
   :align: center

- Click :guilabel:`OK` and save the layer.
- Now that we have calculated the loss value and saved it in a new column,
  we can remove the join.
  Open the layer properties and click the minus button to remove the join
  with BNG_Losses.
- The attribute table when you finish will look like this:

.. image:: /static/training/intermediate/qgis-inasafe/image108.*
   :align: center

**8. Create a Chart**

Now we will conclude by representing these damage and loss values as a chart
in QGIS.

- Go the the properties for the Batas_Desa_Sirahan layer and go to the
  :guilabel:`Overlay` tab.
- Check the box next to :guilabel:`Display diagrams`.
- Make sure :guilabel:`Pie chart` is selected in the dropdown.
- Choose BNG_Dmg next to :guilabel:`Attributes` and click :guilabel:`Add`.
- The following dropdown boxes should read “linearly scaling” and “BNG_Dmg.”
- Click :guilabel:`Find Maximum Value`.
- In the size box enter “500.”

.. image:: /static/training/intermediate/qgis-inasafe/image109.*
   :align: center

- The resulting map will look like this:

.. image:: /static/training/intermediate/qgis-inasafe/image110.*
   :align: center

The size of each bubble represents the loss values in each hamlet.
The bigger the size, the heavier the losses.
Creating a map with this sort of chart can be an effective way to communicate
the impact of a disaster.

In this Module we have learned about methodology for evaluating losses, and we
have learned how to calculate this in QGIS.
We also learned how to export tables, join them with shapefiles,
and overlay charts on top of our map.
