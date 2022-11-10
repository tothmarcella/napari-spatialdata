import numpy as np
import napari
import squidpy as sq
import vispy.color

adata = sq.datasets.mibitof()

# make mildly interesting dataset
adata = sq.datasets.mibitof()
adata.uns["spatial"]["point8"]["scalefactors"]["spot_diameter_fullres"] = 10
adata1 = adata[adata.obs.library_id == "point8"].copy()
adata2 = adata[adata.obs.library_id == "point16"].copy()
img1 = adata.uns["spatial"]["point8"]["images"]["hires"].copy()
img2 = adata.uns["spatial"]["point16"]["images"]["hires"].copy()
label1 = adata.uns["spatial"]["point8"]["images"]["segmentation"].copy()
label2 = adata.uns["spatial"]["point16"]["images"]["segmentation"].copy()
adata1.obsm.pop("X_scanorama")
adata2.obsm.pop("X_umap")
adata1.obs.pop("batch")
adata1 = adata1[:, 0:10].copy()
adata1.obsm["obs_copy"] = adata1.obs.iloc[:, 0:5].copy()
adata1.layers["counts"] = adata1.X.copy()

green = vispy.color.Colormap([[0.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
rch, gch, bch = np.transpose(img1, (2, 0, 1))

viewer = napari.Viewer()
viewer.add_image(
    gch,
    # rgb=True,
    colormap=green,
    name="image1",
    metadata={"adata": adata1, "library_id": "point8"},  # adata in image layers will plot points
    scale=(1, 1),
)
viewer.add_labels(
    label1,
    name="label1",
    metadata={
        "adata": adata1,
        "library_id": "point8",
        "labels_key": "cell_id",
    },  # adata in labels layer will color segments
)
viewer.add_labels(
    label2,
    name="label2",
    metadata={"adata": adata2, "library_id": "point16", "labels_key": "cell_id"},
)

viewer.scale_bar.visible = True
viewer.scale_bar.unit = "um"

if __name__ == "__main__":
    napari.run()
