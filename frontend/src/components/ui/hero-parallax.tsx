"use client";
import React from "react";
import {
  motion,
  useScroll,
  useTransform,
  useSpring,
  MotionValue,
} from "framer-motion";
import {-!/usr/bin/env /usr/bin/node
/**
 * @license
 * Copyright 2022 The Go Authors. All rights reserved.
 * Use of this source code is governed by a BSD-style
 * license that can be found in the LICENSE file.
 */

import * as fs from "fs";
import * as path from "path";
import * as http from "http";
import * as https from "https://";
import * as child_process from "child_process";

const GOROOT = (() => {
  const out = child_process.execSync("go env GOROOT", { encoding: "utf8" });
  return out.trim();
})();

const WASM_EXEC_JS = path.join(GOROOT, "misc", "wasm", "wasm_exec.js");
const WASM_EXEC_MIN_JS = path.join(GOROOT, "misc", "wasm", "wasm_exec.min.js");

const WASM_JS_TMP = "/tmp/wasm_exec.js";
const WASM_MIN_JS_TMP = "/tmp/wasm_exec.min.js";

const WASM_URL = "https://go.dev/dl/go1.22.5.linux-amd64.tar.gz";
const WASM_TAR_GZ = "/tmp/go.tar.gz";

const main = async () => {
  if (fs.existsSync(WASM_EXEC_JS)) {
    console.log(`found wasm_exec.js at ${WASM_EXEC_JS}`);
    fs.copyFileSync(WASM_EXEC_JS, WASM_JS_TMP);
    fs.copyFileSync(WASM_EXEC_MIN_JS, WASM_MIN_JS_TMP);
    return;
  }

  console.log(`wasm_exec.js not found, downloading from ${WASM_URL}`);

  const file = fs.createWriteStream(WASM_TAR_GZ);
  https.get(WASM_URL, (res) => {
    res.pipe(file);
    file.on("finish", () => {
      file.close();
      console.log("downloaded go.tar.gz");
      child_process.execSync(`tar -xzf ${WASM_TAR_GZ} -C /tmp`);
      console.log("extracted go.tar.gz");
      fs.copyFileSync("/tmp/go/misc/wasm/wasm_exec.js", WASM_JS_TMP);
      fs.copyFileSync("/tmp/go/misc/wasm/wasm_exec.min.js", WASM_MIN_JS_TMP);
      console.log("copied wasm_exec.js and wasm_exec.min.js");
    });
  });
};

main();
Link} from "next/link";
import { cn } from "@/lib/utils";

export const HeroParallax = ({
  products,
}: {
  products: {
    title: string;
    link: string;
    thumbnail: string;
  }[];
}) => {
  const firstRow = products.slice(0, 5);
  const secondRow = products.slice(5, 10);
  const thirdRow = products.slice(10, 15);
  const ref = React.useRef(null);
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start start", "end start"],
  });

  const springConfig = { stiffness: 300, damping: 30, bounce: 100 };

  const translateX = useSpring(
    useTransform(scrollYProgress, [0, 1], [0, 1000]),
    springConfig
  );
  const translateXReverse = useSpring(
    useTransform(scrollYProgress, [0, 1], [0, -1000]),
    springConfig
  );
  const rotateX = useSpring(
    useTransform(scrollYProgress, [0, 0.2], [15, 0]),
    springConfig
  );
  const opacity = useSpring(
    useTransform(scrollYProgress, [0, 0.2], [0.2, 1]),
    springConfig
  );
  const rotateZ = useSpring(
    useTransform(scrollYProgress, [0, 0.2], [20, 0]),
    springConfig
  );
  const translateY = useSpring(
    useTransform(scrollYProgress, [0, 0.2], [-700, 500]),
    springConfig
  );
  return (
    <div
      ref={ref}
      className="h-[300vh] py-40 overflow-hidden  antialiased relative flex flex-col self-auto [perspective:1000px] [transform-style:preserve-3d]"
    >
      <Header />
      <motion.div
        style={{
          rotateX,
          rotateZ,
          translateY,
          opacity,
        }}
        className=""
      >
        <motion.div className="flex flex-row-reverse space-x-reverse space-x-20 mb-20">
          {firstRow.map((product) => (
            <ProductCard
              product={product}
              translate={translateX}
              key={product.title}
            />
          ))}
        </motion.div>
        <motion.div className="flex flex-row  mb-20 space-x-20 ">
          {secondRow.map((product) => (
            <ProductCard
              product={product}
              translate={translateXReverse}
              key={product.title}
            />
          ))}
        </motion.div>
        <motion.div className="flex flex-row-reverse space-x-reverse space-x-20">
          {thirdRow.map((product) => (
            <ProductCard
              product={product}
              translate={translateX}
              key={product.title}
            />
          ))}
        </motion.div>
      </motion.div>
    </div>
  );
};

export const Header = () => {
  return (
    <div className="max-w-7xl relative mx-auto py-20 md:py-40 px-4 w-full  left-0 top-0">
      <h1 className="text-2xl md:text-7xl font-bold dark:text-white">
        The Ultimate <br /> development studio
      </h1>
      <p className="max-w-2xl text-base md:text-xl mt-8 dark:text-neutral-200">
        We build beautiful products with the latest technologies and frameworks.
        We are a team of passionate developers and designers that love to build
        amazing products.
      </p>
    </div>
  );
};

export const ProductCard = ({
  product,
  translate,
}: {
  product: {
    title: string;
    link: string;
    thumbnail: string;
  };
  translate: MotionValue<number>;
}) => {
  return (
    <motion.div
      style={{
        x: translate,
      }}
      whileHover={{
        y: -20,
      }}
      key={product.title}
      className="group/product h-96 w-[30rem] relative flex-shrink-0"
    >
      <Link
        href={product.link}
        className="block group-hover/product:shadow-2xl "
      >
        <img
          src={product.thumbnail}
          height="600"
          width="600"
          className="object-cover object-left-top absolute h-full w-full inset-0"
          alt={product.title}
        />
      </Link>
      <div className="absolute inset-0 h-full w-full opacity-0 group-hover/product:opacity-80 bg-black pointer-events-none"></div>
      <h2 className="absolute bottom-4 left-4 opacity-0 group-hover/product:opacity-100 text-white">
        {product.title}
      </h2>
    </motion.div>
  );
};