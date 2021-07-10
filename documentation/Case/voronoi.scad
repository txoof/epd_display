///////////////////////////////////////////////////////////////////////////////
// The Voronoi code below this line is derived from the voronoi code available
// on Thingiverse at http://www.thingiverse.com/thing:47649
//
// (c)2013 Felipe Sanches <juca@members.fsf.org>
// licensed under the terms of the GNU GPL version 3 (or later)

function normalize(v) = v / (sqrt(v[0] * v[0] + v[1] * v[1]));

module voronoi(points, L = 200, thickness = 1, round = 6, nuclei = true) {
	for (p = points) {
		difference() {
			minkowski() {
				intersection_for(p1 = points){
					if (p != p1) {
						angle = 90 + atan2(p[1] - p1[1], p[0] - p1[0]);

						translate((p + p1) / 2 - normalize(p1 - p) * (thickness + round))
						rotate([0, 0, angle])
						translate([-L, -L])
						square([2 * L, L]);
					}
				}
				circle(r = round, $fn = 20);
			}
			if (nuclei)
				translate(p) circle(r = 1, $fn = 20);
		}
	}
}

module my_random_voronoi(   
                            xsize = 100,
                            ysize = 100, 
                            center = false,
                            n = 20,
                            thickness = 1,
                            round = 2,
                            seed = undef)
{
    xmin=0;
    ymin=0;
    L = max(xsize,ysize);
    seed = seed == undef ? rands(0, 100, 1)[0] : seed;
	//echo("Seed", seed);

	// Generate points.
	x = rands(xmin, xsize, n, seed);
	y = rands(ymin, ysize, n, seed + 1);    
	points = [ for (i = [0 : n - 1]) [x[i], y[i]] ];
        
	// Center Voronoi.
	offset_x = center ? -(max(x) - min(x)) / 2 : 0;
	offset_y = center ? -(max(y) - min(y)) / 2 : 0;
    
    intersection()
    {
        square([xsize,ysize],center=center);
        translate([offset_x, offset_y])    
            voronoi(points, L = L, thickness = thickness, round = round, nuclei = false);
    }
}

my_random_voronoi(xsize=100, ysize=100, n=20, round=2, thickness=1, center=true);