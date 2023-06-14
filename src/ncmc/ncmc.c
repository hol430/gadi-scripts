#include <assert.h>
#include <netcdf.h>
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>

// Verbosity level. Set to 1 for verbose builds.
#define VERBOSE 0

typedef struct {
	const char *filename;
	double lat;
	double lon;
} opts_t;

void die(const char *fmt, ...) {
	va_list args;
	va_start(args, fmt);
	vprintf(fmt, args);
	va_end(args);
	printf("\n");
	fflush(stdout);
	exit(1);
}

void parse_args(int argc, char **argv, opts_t *opts) {
	if (argc != 4) {
		die("Usage: %s <latitude> <longitude> <file>", argv[0]);
	}
	double lat, lon;
	sscanf(argv[1], "%lf", &lat);
	sscanf(argv[2], "%lf", &lon);

	opts->lat = lat;
	opts->lon = lon;
	opts->filename = argv[3];
}

void handle_error(int code, const char *fmt, ...) {
	if (code != NC_NOERR) {
		va_list args;
		va_start(args, fmt);
		vprintf(fmt, args);
		va_end(args);
		printf(": ");
		const char *msg = nc_strerror(code);
		die("%s", msg);
	}
}

void log_message(const char *fmt, ...) {
	if (VERBOSE) {
		va_list args;
		va_start(args, fmt);
		vprintf(fmt, args);
		va_end(args);
		printf("\n");
	}
}

void print_opts(const opts_t *opts) {
	log_message("latitude  = %.2f", opts->lat);
	log_message("longitude = %.2f", opts->lon);
	log_message("file      = '%s'", opts->filename);
}

int get_var_id(int nc, int nnames, const char **dim_names, int *iname) {
	if (nnames <= 0) {
		die("No dimension names provided");
	}
	for (int i = 0; i < nnames; i++) {
		const char *name = dim_names[i];
		int varid;
		int err = nc_inq_varid(nc, name, &varid);
		if (err == NC_NOERR) {
			if (iname) {
				*iname = i;
			}
			return varid;
		}
	}
	die("Variable %s does not exist", dim_names[0]);
	return -1; // This will never happen: die() will call exit().
}

void set_dim(int nc, int nnames, const char **dim_names, double newval) {
	int iname;
	int varid = get_var_id(nc, nnames, dim_names, &iname);
	const char *name = dim_names[iname];

	int ndims;
	int err = nc_inq_varndims(nc, varid, &ndims);
	handle_error(err, "Unable to read ndims for variable %s", name);

	if (ndims != 1) {
		die("Variable %s has %d dimensions (expected 1)", name, ndims);
	}

	int dimid;
	err = nc_inq_vardimid(nc, varid, &dimid);
	handle_error(err, "Unable to read dimid for variable %s", name);

	size_t dimlen;
	err = nc_inq_dimlen(nc, dimid, &dimlen);
	handle_error(err, "Unable to read dimension length of %s", name);

	if (dimlen != 1) {
		die("Length of dimension %s is %d (expected 1)", name, dimlen);
	}

	size_t start = 0;
	size_t count = 1;

	double oldval;
	nc_get_vara_double(nc, varid, &start, &count, &oldval);

	log_message("Changing %s from %.2f to %.2f", name, oldval, newval);

	nc_put_vara_double(nc, varid, &start, &count, &newval);
}

int main(int argc, char **argv) {
	opts_t opts;
	parse_args(argc, argv, &opts);
	print_opts(&opts);

	int nc;
	int err = nc_open(opts.filename, NC_WRITE, &nc);
	handle_error(err, "Failed to open %s", opts.filename);

	const char *lat_names[] = { "lat", "latitude" };
	const char *lon_names[] = { "lon", "longitude" };

	set_dim(nc, 2, lat_names, opts.lat);
	set_dim(nc, 2, lon_names, opts.lon);

	err = nc_close(nc);
	handle_error(err, "Failed to close %s", opts.filename);

	return 0;
}
