import glob
import os
import shutil
from urllib.parse import unquote, urlparse

import supervisely as sly
from dataset_tools.convert import unpack_if_archive
from supervisely.io.fs import get_file_name, get_file_name_with_ext
from tqdm import tqdm

import src.settings as s


def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(
            desc=f"Downloading '{file_name_with_ext}' to buffer...",
            total=fsize,
            unit="B",
            unit_scale=True,
        ) as pbar:
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path


def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    ### Function should read local dataset and upload it to Supervisely project, then return project info.###
    dataset_path = "/home/alex/DATASETS/TODO/Meat Cut Image Dataset (BEEF)/Image Dataset/Images"
    ds_name = "ds"
    batch_size = 30

    def create_ann(image_path):
        tags = []

        im_name = get_file_name(image_path)
        if im_name[0] == "b":
            food_type = sly.Tag(background_meta)
            tags.append(food_type)
            timestamp_value = im_name[10:20]
        else:
            food_type = sly.Tag(beef_meta)
            tags.append(food_type)
            timestamp_value = im_name[-10:]
            plant_value = int(im_name[17:20])
            plant = sly.Tag(plant_meta, value=plant_value)
            tags.append(plant)
            product_value = int(im_name[20:25])
            product = sly.Tag(product_meta, value=product_value)
            tags.append(product)
            product_meta_none = product_to_meta.get(product_value)
            product_none = sly.Tag(product_meta_none)
            tags.append(product_none)

        timestamp = sly.Tag(timestamp_meta, value=timestamp_value)
        tags.append(timestamp)

        # image_np = sly.imaging.image.read(image_path)[:, :, 0]
        img_height = 1200  # image_np.shape[0]
        img_wight = 1600  # image_np.shape[1]

        date_value = image_path.split("/")[-2]
        date = sly.Tag(date_meta, value=date_value)
        tags.append(date)

        return sly.Annotation(img_size=(img_height, img_wight), img_tags=tags)

    product_meta = sly.TagMeta("product id", sly.TagValueType.ANY_NUMBER)
    product_20001_meta = sly.TagMeta("Cap Off Pear Off, PAD topside muscle", sly.TagValueType.NONE)
    product_20004_meta = sly.TagMeta("Topside Bullet muscle", sly.TagValueType.NONE)
    product_20003_meta = sly.TagMeta("Topside Heart muscle", sly.TagValueType.NONE)
    product_20010_meta = sly.TagMeta(
        "Cap Off, Non-PAD, Blue Skin Only topside muscle", sly.TagValueType.NONE
    )
    product_20002_meta = sly.TagMeta("Cap off, Pear on topside muscle", sly.TagValueType.NONE)
    product_to_meta = {
        20001: product_20001_meta,
        20002: product_20002_meta,
        20003: product_20003_meta,
        20004: product_20004_meta,
        20010: product_20010_meta,
    }

    plant_meta = sly.TagMeta("plant id", sly.TagValueType.ANY_NUMBER)
    timestamp_meta = sly.TagMeta("timestamp", sly.TagValueType.ANY_STRING)
    background_meta = sly.TagMeta("background", sly.TagValueType.NONE)
    beef_meta = sly.TagMeta("beef", sly.TagValueType.NONE)
    date_meta = sly.TagMeta("date", sly.TagValueType.ANY_STRING)

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(
        tag_metas=[
            product_meta,
            product_20001_meta,
            plant_meta,
            timestamp_meta,
            background_meta,
            beef_meta,
            date_meta,
            product_20004_meta,
            product_20003_meta,
            product_20010_meta,
            product_20002_meta,
        ],
    )
    api.project.update_meta(project.id, meta.to_json())

    dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

    images_pathes = glob.glob(dataset_path + "/*/*.jpg")

    progress = sly.Progress("Create dataset {}".format(ds_name), len(images_pathes))

    for img_pathes_batch in sly.batched(images_pathes, batch_size=batch_size):
        images_names_batch = [get_file_name_with_ext(im_path) for im_path in img_pathes_batch]

        img_infos = api.image.upload_paths(dataset.id, images_names_batch, img_pathes_batch)
        img_ids = [im_info.id for im_info in img_infos]

        anns = [create_ann(image_path) for image_path in img_pathes_batch]
        api.annotation.upload_anns(img_ids, anns)

        progress.iters_done_report(len(images_names_batch))

    return project
