/* (c) 2016++ by Saarbastler 
**  https://github.com/saarbastler/library.scad
**
** Raspberry PI model library for generating cases etc.
*/
$fn=100;

// Which one would you like to see?
part = "piZero"; // [pi3:Raspberry PI3,hifiberryDacPlus:HifiBerry DAC+,pi3_hifiberryDacPlus:Raspberry PI3 & HifiBerry DAC+,piZero:Raspberry PI Zero]

// Show Header
header = true; // true:Show Header;false:Don't show Header

// Header Up/Down for Pi Zero
headerDown = false; //true: Header down (Only Zero): false Header up

module header(pins, rows)
{
  color("darkgrey") cube([2.54*pins,2.54*rows,1.27]);
  
  for(x=[0:pins-1],y=[0:rows-1])
    translate([x*2.54+(1.27+.6)/2,y*2.54+(1.27+.6)/2,-3.5]) cube([0.6,0.6,11.5]);
}

module pi3()
{
  // PCB
  color("limegreen") difference()
  {
    hull()
    {
      translate([-(85-6)/2,-(56-6)/2,0]) cylinder(r=3, h=1.4 );
      translate([-(85-6)/2, (56-6)/2,0]) cylinder(r=3, h=1.4 );
      translate([ (85-6)/2,-(56-6)/2,0]) cylinder(r=3, h=1.4 );
      translate([ (85-6)/2, (56-6)/2,0]) cylinder(r=3, h=1.4 );
    }
    
    translate([-85/2+3.5,-49/2,-1]) cylinder(d=2.75, h=3);
    translate([-85/2+3.5, 49/2,-1]) cylinder(d=2.75, h=3);
    translate([58-85/2+3.5,-49/2,-1]) cylinder(d=2.75, h=3);
    translate([58-85/2+3.5, 49/2,-1]) cylinder(d=2.75, h=3);
  }
  
  // Header
  translate([3.5-85/2+29-10*2.54,49/2-2.54,1.4])
    header(20,2);
  
  translate([-85/2,-56/2,1.4])  
  {
    color("silver") 
    {
      // Ethernet
      translate([85-19,11.5-16/2,0]) cube([21,16,13.8]);
    
      // USB
      translate([85-15, 29-13/2,0]) cube([17,13,15.5]);
      translate([85-15, 47-13/2,0]) cube([17,13,15.5]);
      
      // micro USB
      translate([10.6-8/2,-1.5,0]) cube([8,6,2.6]);
      
      // HDMI
      translate([32-15/2,-1.5,0]) cube([15,11.5,6.6]);
    }
    
    color("darkgrey") 
    {
      // Audio
      translate([53.5-7/2,-2,0]) 
      {
        translate([0,2,0]) cube([7,13,5.6]);
        translate([7/2,0,5.6/2])rotate([-90,0,0]) cylinder(d=5.6,h=2);
      }
    
      // Display
      translate([1.1,(49-22)/2,0]) cube([4,22,5.5]);
      
      // Camera
      translate([45-4/2,1.1,0]) cube([4,22,5.5]);
    }
    
    // Micro SD Card
    color("silver") translate([0,22,-2.9]) cube([13,14,1.5]);    
    color("darkgrey") translate([-2.4,23.5,-2.65]) cube([2.4,11,1]);
  }
}

module hifiberryDacPlus(withHeader=false)
{  
  translate([0,0,13.4])
  {
    // PCB
    color("limegreen") difference()
    {
      translate([(65-85)/2,0,0]) hull()
      {
        translate([-(65-6)/2,-(56-6)/2,0]) cylinder(r=3, h=1.4 );
        translate([-(65-6)/2, (56-6)/2,0]) cylinder(r=3, h=1.4 );
        translate([ (65-6)/2,-(56-6)/2,0]) cylinder(r=3, h=1.4 );
        translate([ (65-6)/2, (56-6)/2,0]) cylinder(r=3, h=1.4 );
      }
      
      translate([-85/2+3.5,-49/2,-1]) cylinder(d=2.75, h=3);
      translate([-85/2+3.5, 49/2,-1]) cylinder(d=2.75, h=3);
      translate([58-85/2+3.5,-49/2,-1]) cylinder(d=2.75, h=3);
      translate([58-85/2+3.5, 49/2,-1]) cylinder(d=2.75, h=3);
    }
    
    // Header down
    translate([3.5-85/2+29-10*2.54,49/2-2.54,-8])
      color("darkgrey") cube([2.54*20,5.08,8]);
    
    // Chinch
    translate([-85/2,-56/2,1.4]) 
    {
      translate([29,0,0]) 
      {
        color("white") cube([10,10,12.5]);        
        color("silver") translate([5,-9,7.5]) rotate([-90,0,0]) cylinder(d=8,h=9);
      }
      translate([46,0,0]) 
      {
        color("red") cube([10,10,12.5]);        
        color("silver") translate([5,-9,7.5]) rotate([-90,0,0]) cylinder(d=8,h=9);
      }
    }
    
    // Header top
    if( withHeader )
      translate([3.5-85/2+29-10*2.54,49/2-2.54-2*2.54,1.4])
        header(20,2);

  }
}

// header: 0 no, 1= up, -1, down
module zero( header= 0)
{
  // PCB
  color("limegreen") difference()
  {
    hull()
    {
      translate([-(65-6)/2,-(30-6)/2,0]) cylinder(r=3, h=1.4 );
      translate([-(65-6)/2, (30-6)/2,0]) cylinder(r=3, h=1.4 );
      translate([ (65-6)/2,-(30-6)/2,0]) cylinder(r=3, h=1.4 );
      translate([ (65-6)/2, (30-6)/2,0]) cylinder(r=3, h=1.4 );
    }
    
    translate([-65/2+3.5,-23/2,-1]) cylinder(d=2.75, h=3);
    translate([-65/2+3.5, 23/2,-1]) cylinder(d=2.75, h=3);
    translate([65/2-3.5,-23/2,-1]) cylinder(d=2.75, h=3);
    translate([65/2-3.5, 23/2,-1]) cylinder(d=2.75, h=3);
  }

  // Header
  if( header == 1)
    translate([3.5-65/2+29-10*2.54,30/2-3.5-2.54,1.4])
      header(20,2);
  if( header == -1)
    translate([3.5-65/2+29-10*2.54,30/2-3.5-2.54,0])
      mirror([0,0,1]) header(20,2);
    
  translate([-65/2,-30/2,1.4])
  {
    // Micro SD Card
    color("silver") translate([1.5,16.9-5,0]) cube([12,10,1.4]);    
    color("darkgrey") translate([-2.5,16.9-5,0.25]) cube([4,10,1]);
    
    // micro USB
    color("silver") translate([41.4-8/2,-1.5,0]) cube([8,6,2.6]);
    color("silver") translate([54-8/2,-1.5,0]) cube([8,6,2.6]);

    // HDMI
    color("silver")  translate([12.4-11.4/2,-.5,0]) cube([11.3,7.5,3.1]);
    
    // Camera
    color("darkgrey") translate([65-3,(30-17)/2,0]) cube([4,17,1.3]);  
  }
}

if( part == "pi3")
  pi3();
else if( part == "hifiberryDacPlus")
  hifiberryDacPlus(header);
else if( part == "pi3_hifiberryDacPlus")
{
  pi3();
  hifiberryDacPlus(header);
}
else if( part == "piZero")
  zero(header ? (headerDown ? -1 : 1) : 0);