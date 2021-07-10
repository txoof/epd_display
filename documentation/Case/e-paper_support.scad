size = [188.5, 138.5]; 
cornerRad = 5;
cutout = [30, size[1]];

mount = [35, 10];

module minsquare(mySize, rad) {
    minsize = [mySize[0]-2*rad, mySize[1]-2*rad];
    translate([-minsize[0]/2, -minsize[1]/2])
    minkowski() {
        square(minsize, center=true);
        translate([minsize[0]/2, minsize[1]/2])
            circle(rad);
    }
}


module back() {
    difference() {
        minsquare(size, cornerRad);
        translate([0, -cutout[1]/2, 0])
            minsquare(cutout, cornerRad);
    }
}

module mounts() {
    translate([-(mount[1]/2+2), 0])
        rotate([0, 0, 90])
        minsquare(mount, cornerRad/2);
    translate([mount[1]/2+2, 0])
        rotate([0, 0, 90])
        minsquare(mount, cornerRad/2);
}

back();
translate([size[0]/2+mount[1]*1.5, mount[0]])
    mounts();
translate([size[0]/2+mount[1]*1.5, 0-5])
    mounts();

//minsquare([100, 50], 5);
