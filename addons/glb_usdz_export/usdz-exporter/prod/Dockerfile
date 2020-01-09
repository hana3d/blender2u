FROM 715293289758.dkr.ecr.us-east-1.amazonaws.com/usdz-exporter:latest

USER root

COPY input/ /usdz-exporter/input/
COPY convert.sh /usr/local/

# CMD tail -f /dev/null
CMD ["/usr/local/convert.sh"]