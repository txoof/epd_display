/*
  Box with fingerjoints - Based on earlier version of Finger Joint Box
  http://www.thingiverse.com/thing:448592
  Aaron Ciuffo
  rewrite to be easier to use as a library
  24 June 2019
*/

/* [Box Dimensions] */
// Box X dimension
customX = 340;
// Box Y dimension
customY = 125;
// Box Z dimension
customZ = 138; //[100.01]

// Finger & Cut width (sides, bottom) - must be < 1/3 shortest side
customFinger = 10;
// Finger & Cut wdith on lid only - must be < 1/3 shortest X or Y
customLidFinger = 20;

// number of internal dividers
customDividers = 2;

// add a lid to the box (set customLidFinger=0 to remove joints along top edge)
customLid = true;

//Material thickness
customMaterial=3; //[0.1:0.05:10]

/* [Layout Option] */
// layout 2D or 3D style - THINGIVERSE CANNOT OUTPUT 2D STLS!
customLayout2D = 1; // [0:3D layout for visualization, 1:2D layout for DXF output]

/* [Hidden] */
// assign the variable for the demo module
/*
tSize=[customX, customY, customZ];
tFinger=customFinger;
tLidFinger=customLidFinger;
tMaterial=customMaterial;
t2D=0;
tAlpha=0.5;
*/


function usableDiv(divs) =
  [divs[0]%2==0 ? divs[0]-3 : divs[0]-2,
   divs[1]%2==0 ? divs[1]-3 : divs[1]-2,
   divs[2]%2==0 ? divs[2]-3 : divs[2]-2];


//calculate max number of fingers and cuts possible
function maxDiv(size, finger) =
  [floor(size[0]/finger),
   floor(size[1]/finger),
   floor(size[2]/finger)];

module insideCuts(length, finger, cutD, div) {
  //make cuts entirely inside the length of the edge
  numFinger = floor(div/2);
  numCuts = ceil(div/2);

  //add a little to the cut depth to avoid Z-Fighting
  myCutD = cutD+0.001;

  //draw rectangeles to make the negative slots
  for (i=[0:numCuts-1]) {
    translate([i*finger*2, 0, 0])
      square([finger, myCutD]);
  }
}

module outsideCuts(length, finger, cutD, div) {
  //make cuts that fall outiside of the edge
  numFinger = ceil(div/2);
  numCuts = floor(div/2);

  //add a little to the cut depth to avoid Z-Fighting
  myCutD = cutD+0.001;

  //calculate the length of the extra long cut at either end of the edge
  endCut = (length-div*finger)/2;

  //amount of padding to add to the itteratigve placement of cuts
  //this is the extra long cut at either end
  padding = endCut+finger;

  square([endCut, myCutD]);

  //draw rectangeles to make the negative slots
  for (i=[0:numCuts]) {
    if (i < numCuts) {
     translate([i*(finger*2)+padding, 0, 0])
        square([finger, myCutD]);
    } else {
      translate([i*finger*2+padding, 0, 0])
        square([endCut, myCutD]);
    }
  }
}


module faceA(size, finger, lidFinger, material, dividers=0) {
  echo("Rendering faceA (X, Z faces)" );
  echo("using size:[0]: ", size[0]," size[2]: ", size[2]);
  maxDivs = maxDiv(size, finger);
  uDiv = usableDiv(maxDivs);
  uDivLid = usableDiv(maxDiv(size, lidFinger));


  difference() {
    square([size[0], size[2]], center=true);
    // X+/- edge (X axis in OpenScad)
    translate([-uDivLid[0]*lidFinger/2, size[2]/2-material, 0])
      insideCuts(length=size[0], finger=lidFinger, cutD=material, div=uDivLid[0]);
   // translate([-uDiv[0]*finger/2, -size[2], 0]
    translate([-uDiv[0]*finger/2, -size[2]/2, 0])
      insideCuts(length=size[0], finger=finger, cutD=material, div=uDiv[0]);

    // Z+/- edge (Y axis)
    translate([size[0]/2-material, uDiv[2]*finger/2, 0])
    rotate([0, 0, -90])
      insideCuts(length=size[2], finger=finger, cutD=material, div=uDiv[2]);

    translate([-size[0]/2, uDiv[2]*finger/2, 0])
    rotate([0, 0, -90])
      insideCuts(length=size[2], finger=finger, cutD=material, div=uDiv[2]);

   if (dividers) {
    // length
    l = size[0]/2;
    // step size
    step = size[0]/(dividers+1);
    for (i = [-l:step:l]) {
      //skip the end dividers; they are not needed (normal walls)
      if (i>-l&&i<l) {
        translate([i+material/2, -uDiv[2]*finger/2, 0])
        rotate([0, 0, 90])
          #insideCuts(length=size[2], finger=finger, cutD=material, div=uDiv[2]);
      }
    }
   }
  }
}



module faceB(size, finger, lidFinger, material, dividers=0, lid=false) {
  echo("Rendering faceB (X, Y Faces)");
  echo("using size:[0]: ", size[0]," size[1]: ", size[1]);
  //lid and base
  maxDivs = lid==true ? maxDiv(size, lidFinger) : maxDiv(size, finger);
  uDiv = usableDiv(maxDivs);

  // divisions for the divider - this is different when a lidFinger value is specified
  maxDividerDivs = maxDiv(size, finger);
  uDividerDiv  = usableDiv(maxDividerDivs);

  myFinger = lid==true ? lidFinger : finger;

  difference() {
    square([size[0], size[1]], center=true);

    //X+/= edge (X axis in view window)
    translate([-size[0]/2, size[1]/2-material, 0])
      outsideCuts(length=size[0], finger=myFinger, cutD=material, div=uDiv[0]);
    translate([-size[0]/2, -size[1]/2, 0])
      outsideCuts(length=size[0], finger=myFinger, cutD=material, div=uDiv[0]);

    //Y+/- edge (Y axis in view window)
    translate([size[0]/2-material, uDiv[1]*myFinger/2, 0])
    rotate([0, 0, -90])
      insideCuts(length=size[1], finger=myFinger, cutD=material, div=uDiv[1]);
    translate([-size[0]/2, uDiv[1]*myFinger/2, 0])
    rotate([0, 0, -90])
      insideCuts(length=size[1], finger=myFinger, cutD=material, div=uDiv[1]);
     if (dividers) {
    // length
    l = size[0]/2;
    // step size
    step = size[0]/(dividers+1);
    for (i = [-l:step:l]) {
      //skip the end dividers; they are not needed (normal +/- X outer walls)
      if (i>-l&&i<l) {
        translate([i+material/2, -uDividerDiv[1]*finger/2, 0])
        rotate([0, 0, 90])
          #insideCuts(length=size[1], finger=finger, cutD=material, div=uDividerDiv[1]);
      }
    }
   }
  }
}



module faceC(size, finger, lidFinger, material) {
  echo("Rendering faceB (Y, Z Faces)");
  echo("using size:[1]: ", size[1]," size[2]: ", size[2]);
  maxDivs = maxDiv(size, finger);
  uDiv = usableDiv(maxDivs);
  uDivLid = usableDiv(maxDiv(size, lidFinger));

  difference() {
    square([size[1], size[2]], center=true);

    //Y+/- edge (X asis in view window)
    translate([-size[1]/2, size[2]/2-material, 0])
      outsideCuts(length=size[1], finger=lidFinger, cutD=material, div=uDivLid[1]);
    translate([-size[1]/2, -size[2]/2, 0])
      outsideCuts(length=size[1], finger=finger, cutD=material, div=uDiv[1]);

    //Z+/- edge (Y axis in view window)
    translate([size[1]/2-material, size[2]/2, 0])
    rotate([0, 0, -90])
      outsideCuts(length=size[2], finger=finger, cutD=material, div=uDiv[2]);
    translate([-size[1]/2, size[2]/2, 0])
    rotate([0, 0, -90])
      outsideCuts(length=size[2], finger=finger, cutD=material, div=uDiv[2]);
  }
}

//divider(myS, myF, m, true);

//internal divider 
module divider(size, finger, material, lid=true) {

  maxDivs = maxDiv(size, finger);
  uDiv = usableDiv(maxDivs);

  difference() {
    square([size[1], size[2]], center=true);

    //Y+/- edge
    if(!lid) {
      // remove a bit from the top to avoid an interface w/ the lid
      translate([-size[1]/2, size[2]/2-material])
        outsideCuts(length=size[1], finger=finger, cutD=material, div=uDiv[1]);
    } else {
      translate([0, size[2]/2-material/2])
        square([size[1], material], center=true);
    }

    translate([-size[1]/2, -size[2]/2])
      outsideCuts(length=size[1], finger=finger, cutD=material, div=uDiv[1]);

    //Z+/- edge
    translate([-size[1]/2, size[2]/2])
    rotate([0, 0, -90])
      outsideCuts(length=size[2], finger=finger, cutD=material, div=uDiv[2]);
    translate([size[1]/2-material, size[2]/2])
    rotate([0, 0, -90])
      outsideCuts(length=size[2], finger=finger, cutD=material, div=uDiv[2]);
  }
// this is code is for making the corresponding cuts in the other faces
//  translate([size[1]/2-material, uDiv[2]*finger/2])
//  rotate([0, 0, -90])
//    #insideCuts(length=size[2], finger=finger, cutD=material, div=uDiv[2]);

}

module layout(size, material, 2D=true, alpha=0.5, dividers=0, v=true) {

  if (v) {
    echo("parameters:"); echo("material (thickness of material)");
    echo("size ([X, Y, Z] - dimensions of box)");
    echo("2D (boolean - childrender in 2D or 3D)");
    echo("alpha (real between 0, 1 - transparency of 3D model)");
    echo(" ");
    echo("requires six children faces provided in the order below");
    echo("face relative XYZs are shown along with childrendering colors");
    echo("layout2D() { faceA(-XZ red); faceA(+XZ darkred); faceB(-XY lime); faceB(+XY green); faceC(-YZ blue); faceC(+YZ darkblue);}");
  }

  if(2D) {
    //separation of pieces for 2D layout
    separation = 1.5;
    //calculate the most efficient layout for 2D layout
    yDisplace = size[1] > size[2] ? size[1] : size[2] + separation;


    translate([0, 0, 0])
      color("Red")
      //faceA(size=size, finger=finger, material=material, lidFinger=lidFinger);
      children(0);

    translate([size[0]+separation+size[1]+separation, 0, 0])
      color("darkred")
      //faceA(size=size, finger=finger, material=material, lidFinger=lidFinger);
      children(1);

    translate([size[0]/2+size[1]/2+separation, 0, 0])
      color("blue")
      //faceC(size=size, finger=finger, material=material, lidFinger=lidFinger);
      children(4);

    translate([size[0]/2+size[1]/2+separation, -yDisplace, 0])
      color("darkblue")
      //faceC(size=size, finger=finger, material=material, lidFinger=lidFinger);
      children(5);


    translate([0, -size[2]/2-yDisplace/2-separation, 0])
      color("lime")
      //faceB(size=size, finger=finger, material=material, lidFinger=lidFinger, lid=true);
      children(2);

    translate([size[0]+separation+size[1]+separation, -size[2]/2-yDisplace/2-separation, 0])
      color("green")
      //faceB(size=size, finger=finger, material=material, lidFinger=lidFinger);
      children(3);

    for (i=[0:dividers-1]) {
      translate([(i*size[1])+separation*i, size[2]+separation, 0])
        color("purple")
        children(6);
    }

  } else {
    //draw 3d model
    //amount to shift to account for thickness of material
    D = material/2;

    //base
    color("green", alpha=alpha)
      translate([0, 0, 0])
      linear_extrude(height=material, center=true)
        //faceB(size=size, finger=finger, material=material, lidFinger=lidFinger);
        children(2);

    //lid
    color("lime", alpha=alpha)
      translate([0, 0, size[2]-material])
      linear_extrude(height=material, center=true)
        //faceB(size=size, finger=finger, material=material, lidFinger=lidFinger, lid=true);
        children(3);

    color("red", alpha=alpha)
      translate([0, size[1]/2-D, size[2]/2-D])
      rotate([90, 0, 0])
      linear_extrude(height=material, center=true)
        //faceA(size=size, finger=finger, material=material, lidFinger=lidFinger);
        children(0);

    color("darkred", alpha=alpha)
      translate([0, -size[1]/2+D, size[2]/2-D])
      rotate([90, 0, 0])
      linear_extrude(height=material, center=true)
        //faceA(size=size, finger=finger, material=material, lidFinger=lidFinger);
        children(1);

    color("blue", alpha=alpha)
      translate([size[0]/2-D, 0, size[2]/2-D])
      rotate([90, 0, 90])
      linear_extrude(height=material, center=true)
        //faceC(size=size, finger=finger, material=material, lidFinger=lidFinger);
        children(4);


    color("darkblue", alpha=alpha)
      translate([-size[0]/2+D, 0, size[2]/2-D])
      rotate([90, 0, 90])
      linear_extrude(height=material, center=true)
        //faceC(size=size, finger=finger, material=material, lidFinger=lidFinger);
        children(5);
    // add dividers
     if (dividers) {
      // length
      l = size[0]/2;
      // step size
      step = size[0]/(dividers+1);
      for (i = [-l:step:l]) {
        //skip the end dividers; they are not needed (normal walls)
        if (i>-l&&i<l) {
          color("purple", alpha=alpha)
          translate([i, 0, size[2]/2-D])
          rotate([90, 0, 90])
            linear_extrude(height=material, center=true)
            children(6);
        }
      }
     }
  }
}


myS = [customX, customY, customZ];
myF = customFinger;
myLF = customLidFinger;
myMat = customMaterial;
myDiv = customDividers;
myLid = customLid;
myLayout = customLayout2D; 
//myLayout = false;

layout(size=myS, material=myMat, 2D=myLayout, dividers=myDiv) {
  faceA(myS, myF, myLF, myMat, myDiv);
  faceA(myS, myF, myLF, myMat, dividers=myDiv);
  faceB(myS, myF, myLF, myMat, dividers=myDiv, lid=false);
  faceB(myS, myF, myLF, myMat, dividers=myDiv, lid=myLid);
  faceC(myS, myF, myLF, myMat);
  faceC(myS, myF, myLF, myMat);
  divider(myS, myF, myMat, lid=myLid);
}

/*
To Do:
* lid is using the lidfinger division values for making the finger holes in lid

*/

